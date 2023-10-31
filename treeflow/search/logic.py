from typing import List, Dict, Union, Optional
from django.core.exceptions import EmptyResultSet
from django.db.models import Subquery, OuterRef, Max, F, Q, Count, Exists
from treeflow.corpus.models import Section, Token, SectionToken
from treeflow.corpus.types.token import TokenSearchInput
from treeflow.corpus.types.section import HighlightedSection
from treeflow.corpus.types.text import Text
from strawberry import relay
from collections import defaultdict
import logging
import time
from functools import reduce
import operator

logger = logging.getLogger(__name__)

def build_query_for_criteria(criteria: TokenSearchInput, number: Optional[int] = None) -> Q:
    # Start with the base criteria if its value is not None
    if criteria.value is not None:
        query = Q(**{f"{criteria.field}__{criteria.query_type}": criteria.value})
    else:
        query = Q()  # Base empty Q object
    
    # POS criteria
    if criteria.pos_token:
        pos_queries = [Q(pos_token__pos=pos_input.pos) for pos_input in criteria.pos_token]
        query &= reduce(operator.or_, pos_queries)
    
    # Feature criteria
    if criteria.feature_token:
        feature_queries = []
        for feature_input in criteria.feature_token:
            feature_q = Q(feature_token__feature=feature_input.feature)
            if feature_input.feature_value:
                feature_q &= Q(feature_token__feature_value=feature_input.feature_value)
            feature_queries.append(feature_q)
        query &= reduce(operator.or_, feature_queries)
    
    # TODO: Add similar logic for lemmas and meanings once their schema and relationships are known
    
    # Number criteria (distance and position)
    if number is not None:
        if criteria.distance and not criteria.distance.exact:
            if criteria.distance.type == "after":
                query &= Q(number__gte=number)
            elif criteria.distance.type == "before":
                query &= Q(number__lte=number)
        else:
            query &= Q(number=number)

    logger.debug(f"Built query for criteria: {query}")
    return query


    
def execute_query(query: Q) -> List[Token]:
    token_objects = Token.objects.filter(query)
    query_string = str(token_objects.query)  # Convert the SQL query to a string representation for logging
    logger.debug(f"Executing SQL query: {query_string}")
    
    matching_tokens = list(token_objects)  # Convert the queryset to a list of tokens
    
    number_of_results = len(matching_tokens)  # Count the number of tokens that match the query
    logger.debug(f"Number of tokens found for query {query}: {number_of_results}")
    
    if number_of_results == 0:
        logger.warning(f"No tokens found for query: {query}")
    
    return matching_tokens

def search_tokens_for_single_anchor(anchor_token: Token, criteria_list: List[TokenSearchInput]) -> List[Token]:
    logger.debug(f"Searching tokens for anchor: {anchor_token}")
    matched_tokens = [anchor_token]
    current_number = anchor_token.number

    # Iterate over the rest of the criteria_list
    for criteria in criteria_list[1:]:
        logger.debug(f"Processing criteria: {criteria}")
        # Determine the expected position of the token
        if criteria.distance.type == "after":
            current_number += criteria.distance.distance
        else:
            current_number = matched_tokens[-1].number - criteria.distance.distance
        
        # Build and execute query
        token_query = build_query_for_criteria(criteria, current_number)
        logger.debug(f"Built query: {token_query}")
        tokens = execute_query(token_query)
        
        # Check if any tokens matched the criteria
        if not tokens:
            logger.warning(f"No tokens found for criteria: {criteria}. Breaking sequence for anchor: {anchor_token}.")
            return []
        
        # For simplicity, we're assuming that the first token in the list is the desired match.
        # Adjustments may be needed if other criteria for selecting a token from the list are required.
        token = tokens[0]
        logger.debug(f"Using token: {token} from {len(tokens)} potential matches.")
        matched_tokens.append(token)

    logger.debug(f"Completed sequence for anchor: {anchor_token}. Tokens: {matched_tokens}")
    return matched_tokens


def search_tokens_in_sequence(criteria_list: List[TokenSearchInput], texts: List[str] = None) -> List[List[Token]]:
    logger.info("Starting search_tokens_in_sequence.")
    # Fetch all appearances of the anchor token
    anchor_token_query = build_query_for_criteria(criteria_list[0])
    
    # If texts are provided, filter the tokens based on the provided text IDs
    if texts:
        anchor_tokens = Token.objects.filter(anchor_token_query, text_id__in=texts).all()
    else:
        anchor_tokens = Token.objects.filter(anchor_token_query).all()
    
    logger.debug(f"Found {len(anchor_tokens)} anchor tokens")
    
    all_matched_sequences = []
    # For each anchor token, try to find a matching sequence
    for anchor_token in anchor_tokens:
        logger.debug(f"Processing anchor token: {anchor_token}")
        matched_sequence = search_tokens_for_single_anchor(anchor_token, criteria_list)
        if matched_sequence:
            all_matched_sequences.append(matched_sequence)

    logger.info(f"Finished search_tokens_in_sequence. Total sequences found: {len(all_matched_sequences)}")
    return all_matched_sequences

def get_sections_for_matched_tokens(criteria_list: List[TokenSearchInput], section_type: str, texts: Optional[List[str]] = None) -> List[HighlightedSection]:

    time_start = time.time()
    logger.info("Starting get_sections_for_matched_tokens.")
    
    # Obtain the list of matched token sequences
    matched_token_sequences = search_tokens_in_sequence(criteria_list, texts)
    
    logger.debug(f"Number of matched token sequences: {len(matched_token_sequences)}")
    
    matched_highlighted_sections = []

    # Gather all tokens from the matched sequences
    all_tokens = [token for sequence in matched_token_sequences for token in sequence]

    # Initial query for SectionTokens based on the matched tokens and section_type
    section_tokens_query = SectionToken.objects.filter(token__in=all_tokens, section__type=section_type).select_related('section')

    # If specific texts are provided, further filter the query
    if texts:
        section_tokens_query = section_tokens_query.filter(section__text_id__in=texts)

    # Create a dictionary to map sections to tokens
    section_to_tokens = defaultdict(list)
    for section_token in section_tokens_query:
        section_to_tokens[section_token.section].append(section_token.token)

    # Create HighlightedSection objects
    for section, tokens in section_to_tokens.items():
        matched_highlighted_sections.append(HighlightedSection(section=section, highlighted_tokens=tokens))
        logger.debug(f"Found section {section} with tokens: {tokens}")

    logger.info(f"Finished get_sections_for_matched_tokens. Total sections found: {len(matched_highlighted_sections)}")
    time_end = time.time()
    logger.info(f"Time elapsed: {time_end - time_start} seconds")
    return matched_highlighted_sections


