from typing import List, Dict, Union, Optional
from django.core.exceptions import EmptyResultSet
from django.db.models import Subquery, OuterRef, Max, F, Q, Count, Exists, Prefetch
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
from itertools import chain
import json

logger = logging.getLogger(__name__)


def token_search_input_to_dict(token_search_input: TokenSearchInput) -> dict:
    """Convert a TokenSearchInput object into a dictionary."""
    return {
        "query_type": token_search_input.query_type,
        "value": token_search_input.value,
        "field": token_search_input.field,
        "pos_token": [vars(pos) for pos in (token_search_input.pos_token or [])],
        "feature_token": [vars(feature) for feature in (token_search_input.feature_token or [])],
        "lemmas": [vars(lemma) for lemma in (token_search_input.lemmas or [])],
        "meanings": [vars(meaning) for meaning in (token_search_input.meanings or [])],
        "stopwords": token_search_input.stopwords,
        "distance": vars(token_search_input.distance) if token_search_input.distance else None
    }

def token_search_input_to_key(token_search_input: TokenSearchInput) -> str:
    """Convert a TokenSearchInput object into a string key."""
    return json.dumps(token_search_input_to_dict(token_search_input), sort_keys=True)


def build_query_for_criteria(criteria: TokenSearchInput, number: Optional[int] = None) -> Q:
    if criteria.value is not None:
        query = Q(**{f"{criteria.field}__{criteria.query_type}": criteria.value})
    else:
        query = Q()
    
    if criteria.pos_token:
        pos_queries = [Q(pos_token__pos=pos_input.pos) for pos_input in criteria.pos_token]
        query &= reduce(operator.or_, pos_queries)
    
    if criteria.feature_token:
        feature_queries = []
        for feature_input in criteria.feature_token:
            feature_q = Q(feature_token__feature=feature_input.feature)
            if feature_input.feature_value:
                feature_q &= Q(feature_token__feature_value=feature_input.feature_value)
            feature_queries.append(feature_q)
        query &= reduce(operator.or_, feature_queries)

    if criteria.lemmas:
        lemma_queries = []
        for lemma_input in criteria.lemmas:
            lemma_q = Q()
            if lemma_input.word:
                lemma_q &= Q(lemmas__word=lemma_input.word)
            if lemma_input.language:
                lemma_q &= Q(lemmas__language=lemma_input.language)
            lemma_queries.append(lemma_q)
        query &= reduce(operator.or_, lemma_queries)

    if criteria.meanings:
        meaning_queries = []
        for meaning_input in criteria.meanings:
            meaning_q = Q()
            if meaning_input.meaning:
                meaning_q &= Q(meanings__meaning=meaning_input.meaning)
            if meaning_input.language:
                meaning_q &= Q(meanings__language=meaning_input.language)
            meaning_queries.append(meaning_q)
        query &= reduce(operator.or_, meaning_queries)
    
    if number is not None and criteria.distance:
        if not criteria.distance.exact:
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
    query_string = str(token_objects.query)
    logger.debug(f"Executing SQL query: {query_string}")
    
    matching_tokens = list(token_objects)
    number_of_results = len(matching_tokens)
    logger.debug(f"Number of tokens found for query {query}: {number_of_results}")
    
    if number_of_results == 0:
        logger.warning(f"No tokens found for query: {query}")
    
    return matching_tokens

def single_criterion_processing(criteria, texts=None):
    logger.debug(f"Processing single criterion: {criteria}")
    token_query = build_query_for_criteria(criteria)
    return [[token] for token in fetch_tokens(token_query, texts)]


def fetch_tokens(query, texts=None):
    if texts:
        return list(Token.objects.filter(query, text_id__in=texts))
    return list(Token.objects.filter(query))

def fetch_anchor_tokens(criteria_list, texts=None):
    anchor_token_query = build_query_for_criteria(criteria_list[0])
    logger.debug(f"Constructed anchor token query: {anchor_token_query}")
    return fetch_tokens(anchor_token_query, texts)


def process_batch(anchor_tokens, batch_size):
    batches = []
    for i in range(0, len(anchor_tokens), batch_size):
        batched_anchors = anchor_tokens[i:i+batch_size]
        logger.debug(f"Processing batch {i//batch_size + 1} of anchor tokens, size: {len(batched_anchors)}")
        batches.append(batched_anchors)
    return batches


def search_tokens_for_anchor_sequence(anchor_token: Token, criteria_list: List[TokenSearchInput], texts=None) -> List[Token]:
    logger.debug(f"Searching tokens for anchor: {anchor_token}")
    
    # Initialize the matched tokens list with the anchor token
    matched_tokens = [anchor_token]
    
    # If there's only one criterion, process it using a single criterion processor
    if len(criteria_list) == 1:
        return single_criterion_processing(criteria_list[0], texts)
    
    # Iterate over the criteria_list
    for criteria in criteria_list[1:]:
        logger.debug(f"Processing criteria: {criteria}")
        
        # Determine the expected position of the token
        current_number = matched_tokens[-1].number
        if criteria.distance.type == "after":
            current_number += criteria.distance.distance
        else:
            current_number -= criteria.distance.distance
        
        # Build and execute the token query
        token_query = build_query_for_criteria(criteria, current_number)
        tokens = execute_query(token_query)
        
        # Check if any tokens matched the criteria
        if not tokens:
            logger.warning(f"No tokens found for criteria: {criteria}. Breaking sequence for anchor: {anchor_token}.")
            return []
        
        # Assuming the first token in the list is the desired match
        token = tokens[0]
        logger.debug(f"Using token: {token} from {len(tokens)} potential matches.")
        matched_tokens.append(token)
    
    logger.debug(f"Completed sequence for anchor: {anchor_token}. Tokens: {matched_tokens}")
    return matched_tokens

def construct_queries_for_batch(batched_anchors, criteria):
    """Constructs token queries for all anchors in the current batch."""
    logger.debug(f"Constructing queries for {len(batched_anchors)} anchors.")
    
    # Ensure that batched_anchors is a list of lists
    if not isinstance(batched_anchors[0], list):
        batched_anchors = [batched_anchors]
    
    all_anchors = list(chain.from_iterable(batched_anchors))
    
    return [build_query_for_criteria(criteria, anchor_token.number) for anchor_token in all_anchors]

def map_tokens_to_anchors(matched_tokens, batched_anchors, criteria):
    """Maps tokens to their respective anchors based on the given criteria."""
    logger.debug("Mapping tokens to their respective anchors.")
    token_to_anchor = {}
    for token in matched_tokens:
        closest_anchor = min(batched_anchors, key=lambda a: abs(a.number - token.number))
        
        condition_met = False
        if criteria.distance.type == 'after':
            if criteria.distance.exact:
                condition_met = 0 < (token.number - closest_anchor.number) <= criteria.distance.distance
            else:
                condition_met = 0 < (token.number - closest_anchor.number)
        elif criteria.distance.type == 'before':
            if criteria.distance.exact:
                condition_met = 0 < (closest_anchor.number - token.number) <= criteria.distance.distance
            else:
                condition_met = 0 < (closest_anchor.number - token.number)
        
        if condition_met:
            token_to_anchor[token.id] = closest_anchor
            logger.debug(f"Token {token.id} mapped to anchor {closest_anchor.id}")
        else:
            logger.debug(f"Token {token.id} not mapped due to criteria not met.")
    
    return token_to_anchor

def process_criteria_for_batch(batched_anchors, criteria):
    """Processes the criteria for the given batch of anchor tokens."""
    logger.debug(f"Processing criteria: {criteria} for batch of {len(batched_anchors)} anchors.")
    token_queries = construct_queries_for_batch(batched_anchors, criteria)
    combined_query = reduce(operator.or_, token_queries)
    logger.debug(f"Executing combined query: {combined_query}")
    matched_tokens = execute_query(combined_query)
    logger.debug(f"Found {len(matched_tokens)} tokens matching combined query.")
    return map_tokens_to_anchors(matched_tokens, batched_anchors, criteria)

def search_tokens_in_sequence(criteria_list: List[TokenSearchInput], texts: List[str] = None, batch_size: int = 1000) -> List[List[Token]]:
    logger.info(f"Starting search_tokens_in_sequence with {len(criteria_list)} criteria.")
    time_start = time.time()
    # If only one criterion, process it and return
    if len(criteria_list) == 1:
        criteria = criteria_list[0]
        logger.debug(f"Processing single criterion: {criteria}")
        token_query = build_query_for_criteria(criteria)
        matching_tokens = fetch_tokens(token_query, texts)
        logger.debug(f"Found {len(matching_tokens)} tokens for the single criterion.")
        return [[token] for token in matching_tokens]
    
    anchor_tokens = fetch_anchor_tokens(criteria_list, texts)
    logger.debug(f"Found {len(anchor_tokens)} anchor tokens.")
    
    all_matched_sequences = []

    # Split the anchor tokens into batches for processing
    for i in range(0, len(anchor_tokens), batch_size):
        batched_anchors = anchor_tokens[i: i + batch_size]
        
        # Initialize the dictionary with the anchor tokens
        anchor_to_sequence = {anchor: [anchor] for anchor in batched_anchors}
        
        # Iterate over the criteria_list to match tokens for each anchor token
        for criteria in criteria_list[1:]:
            token_queries = construct_queries_for_batch(batched_anchors, criteria)
            token_to_anchor = process_criteria_for_batch(batched_anchors, criteria)
            
            for token, anchor in token_to_anchor.items():
                anchor_to_sequence[anchor].append(token)  # Add matched tokens to sequences of their respective anchors

        # Filter out any sequences that only contain the anchor token
        matched_sequences_in_batch = [sequence for sequence in anchor_to_sequence.values() if len(sequence) > 1]
        logger.debug(f"Sequences matched in this batch: {len(matched_sequences_in_batch)}")
        all_matched_sequences.extend(matched_sequences_in_batch)

    logger.info(f"Finished search_tokens_in_sequence. Total sequences found: {len(all_matched_sequences)}")
    time_end = time.time()
    logger.info(f"Time elapsed: {time_end - time_start} seconds")
    return all_matched_sequences


def get_sections_for_matched_tokens(criteria_list: List[TokenSearchInput], section_type: str, texts: Optional[List[str]] = None) -> List[HighlightedSection]:
    time_start = time.time()
    logger.info("Starting get_sections_for_matched_tokens.")
    
    # Obtain the list of matched token sequences
    matched_token_sequences = search_tokens_in_sequence(criteria_list, texts)
    logger.debug(f"Number of matched token sequences: {len(matched_token_sequences)}")
    
    # Flatten the list of matched token sequences and extract only the IDs
    all_token_ids = [token.id if hasattr(token, 'id') else token for sequence in matched_token_sequences for token in sequence]

    # Prefetch SectionTokens with related tokens based on the matched token IDs
    section_token_prefetch = Prefetch(
        'sectiontoken_set',
        queryset=SectionToken.objects.filter(token_id__in=all_token_ids).select_related('token'),
        to_attr='related_section_tokens'
    )

    # Fetch sections based on section_type and optional texts, and prefetch the related tokens
    sections_query = Section.objects.filter(type=section_type, sectiontoken__token_id__in=all_token_ids).distinct().prefetch_related(section_token_prefetch)
    if texts:
        sections_query = sections_query.filter(text_id__in=texts)
    sections_with_tokens = list(sections_query)

    # Create HighlightedSection objects based on the fetched tokens
    matched_highlighted_sections = [
        HighlightedSection(section=section, highlighted_tokens=[st.token for st in section.related_section_tokens])
        for section in sections_with_tokens if hasattr(section, 'related_section_tokens') and section.related_section_tokens
    ]

    # Check if there's more than one token in the criteria
    if len(criteria_list) > 1:
        # After creating the matched_highlighted_sections
        for highlighted_section in matched_highlighted_sections:
            token_ids_in_section = set([token.id for token in highlighted_section.highlighted_tokens])
            for sequence in matched_token_sequences:
                sequence_token_ids = set([token.id if hasattr(token, 'id') else token for token in sequence])
                if not sequence_token_ids.issubset(token_ids_in_section):
                    # This means not all tokens from this sequence are in the section
                    highlighted_section.feedback = f"Tokens {sequence_token_ids - token_ids_in_section} are not present in the section."
                    break

    logger.info(f"Finished get_sections_for_matched_tokens. Total sections found: {len(matched_highlighted_sections)}")
    time_end = time.time()
    logger.info(f"Time elapsed: {time_end - time_start} seconds")
    return matched_highlighted_sections


