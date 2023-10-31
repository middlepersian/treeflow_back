from typing import List, Dict, Union, Optional
from django.core.exceptions import EmptyResultSet
from django.db.models import Subquery, OuterRef, Max, F, Q, Count, Exists
from treeflow.corpus.models import Section, Token, SectionToken
from treeflow.corpus.types.token import TokenSearchInput
from treeflow.corpus.types.text import Text
from strawberry import relay
from collections import defaultdict
import logging
import time
from functools import reduce
import operator

logger = logging.getLogger(__name__)

def build_query_for_criteria(criteria: TokenSearchInput, number: Optional[int] = None) -> Q:
    query = Q(**{f"{criteria.field}__{criteria.query_type}": criteria.value})
    
    if number is not None:
        if criteria.distance and not criteria.distance.exact:
            if criteria.distance.type == "after":
                query &= Q(number__gte=number)
            else:
                query &= Q(number__lte=number)
        else:
            query &= Q(number=number)

    logger.debug(f"Built query for criteria: {query}")
    return query

def execute_query(query: Q) -> Optional[Token]:
    token_objects = Token.objects.filter(query)
    logger.debug(f"Executing SQL query: {token_objects.query}")
    token = token_objects.first()
    if token:
        logger.debug(f"Found token for query {query}: {token}")
    else:
        logger.warning(f"No token found for query: {query}")
    return token

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
        token = execute_query(token_query)
        
        if not token:
            logger.warning(f"Token not found for criteria: {criteria}. Breaking sequence for anchor: {anchor_token}.")
            return []
        logger.debug(f"Found token: {token}")
        matched_tokens.append(token)

    logger.debug(f"Completed sequence for anchor: {anchor_token}. Tokens: {matched_tokens}")
    return matched_tokens

def search_tokens_in_sequence(criteria_list: List[TokenSearchInput]) -> List[List[Token]]:
    logger.info("Starting search_tokens_in_sequence.")
    # Fetch all appearances of the anchor token
    anchor_token_query = build_query_for_criteria(criteria_list[0])
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

def get_sections_for_matched_tokens(criteria_list: List[TokenSearchInput]) -> List[Section]:
    logger.info("Starting get_sections_for_matched_tokens.")
    
    # Obtain the list of matched token sequences
    matched_token_sequences = search_tokens_in_sequence(criteria_list)
    
    logger.debug(f"Number of matched token sequences: {len(matched_token_sequences)}")
    
    matched_sections = set()
    # For each token sequence in the matched token sequences
    for token_sequence in matched_token_sequences:
        logger.debug(f"Processing token sequence: {token_sequence}")
        # For each token in the token sequence, fetch the related sections
        for token in token_sequence:
            for section_token in SectionToken.objects.filter(token=token):
                matched_sections.add(section_token.section)
                logger.debug(f"Found section for token {token}: {section_token.section}")

    logger.info(f"Finished get_sections_for_matched_tokens. Total sections found: {len(matched_sections)}")
    return list(matched_sections)
