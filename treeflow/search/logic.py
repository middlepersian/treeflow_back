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

def search_tokens_in_sequence(criteria_list: List[TokenSearchInput]) -> List[Token]:
    logger.debug(f"####     search_tokens_in_sequence      ####")
    start_time = time.time()

    matched_tokens = []

    # Fetch the anchor token
    anchor_token_query = build_query_for_criteria(criteria_list[0])
    anchor_token = execute_query(anchor_token_query)
    
    if not anchor_token:
        logger.warning("Anchor token not found.")
        return []
    
    matched_tokens.append(anchor_token)
    current_number = anchor_token.number

    # Iterate over the rest of the criteria_list
    for idx in range(1, len(criteria_list)):
        criteria = criteria_list[idx]
        
        # Determine the expected position of the token
        if criteria.distance.type == "after":
            current_number += criteria.distance.distance
        else:
            # When looking for a token before another, compute its position relative to the last matched token
            current_number = matched_tokens[-1].number - criteria.distance.distance

        # Build and execute query based on its characteristics and position
        token_query = build_query_for_criteria(criteria, current_number)
        token = execute_query(token_query)
        
        if not token:
            logger.warning(f"Token not found for criteria {idx + 1}.")
            break  # Break out of the loop, but don't return yet

        matched_tokens.append(token)

    # log the time
    logger.debug(f"Time taken to fetch tokens: {time.time() - start_time} seconds")   

    return matched_tokens



def get_sections_for_matched_tokens(criteria_list: List[TokenSearchInput]) -> List[Section]:
    logger.debug(f"####     get_sections_for_matched_tokens     ####")
    #log the start time
    start_time = time.time()
    # Obtain the list of matched tokens using the search_tokens_in_sequence method
    matched_tokens = search_tokens_in_sequence(criteria_list)
    
    # Initialize a set to store unique sections
    matched_sections = set()
    
    # For each token in the matched tokens list, fetch the related sections and add them to the set
    for token in matched_tokens:
        for section_token in SectionToken.objects.filter(token=token):
            matched_sections.add(section_token.section)
    
    # Log the time taken to fetch the sections
    logger.debug(f"Time taken to fetch sections: {time.time() - start_time} seconds")
    # Convert the set to a list and return
    return list(matched_sections)
