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
from decimal import Decimal

logger = logging.getLogger(__name__)


from typing import List

def retrieve_initial_anchors(criterion: TokenSearchInput) -> List[Token]:
    """
    Retrieve all tokens that match the given criterion.
    These tokens will act as potential anchors for further search.

    :param criterion: The TokenSearchInput object containing the search criterion.
    :return: A list of Token objects that match the criterion.
    
    """

    tokens = Token.objects.none()  # This will create an empty queryset
    # Assuming criterion.value contains the text to match and criterion.field is the field to search in
    if criterion.query_type == 'exact':
        tokens = Token.objects.filter(**{f'{criterion.field}__iexact': criterion.value})
    elif criterion.query_type == 'contains':
        tokens = Token.objects.filter(**{f'{criterion.field}__icontains': criterion.value})
    # Add more conditions for different query types if necessary

    # Now you have a queryset of tokens that match the criterion, which are your initial anchors
    return list(tokens)


def identify_candidate_sections(anchors: List[Token]) -> List[Section]:
    """
    Identify distinct sections from a list of anchor tokens.

    :param anchors: A list of Token objects to find the sections for.
    :return: A list of unique Section objects that are associated with the tokens.
    """
    # Using a set to avoid duplicate sections
    section_ids = set()
    for token in anchors:
        # Assuming that each token has a foreign key to a SectionToken which in turn is related to a Section
        section_tokens = token.sectiontoken_set.all()
        for section_token in section_tokens:
            section_ids.add(section_token.section_id)

    # Now retrieve Section objects based on the collected section IDs
    candidate_sections = Section.objects.filter(id__in=section_ids)
    return list(candidate_sections)

def apply_criterion(queryset, criterion):
    # This function applies the specific criterion to the queryset and returns the modified queryset.
    field_query = f"sectiontoken__token__{criterion.field}__"

    if criterion.query_type == 'exact':
        return queryset.filter(**{f'{field_query}iexact': criterion.value})
    elif criterion.query_type == 'not':
        return queryset.exclude(**{f'{field_query}iexact': criterion.value})
    elif criterion.query_type == 'contains':
        return queryset.filter(**{f'{field_query}icontains': criterion.value})
    elif criterion.query_type == 'not_contains':
        return queryset.exclude(**{f'{field_query}icontains': criterion.value})
    elif criterion.query_type == 'regex':
        return queryset.filter(**{f'{field_query}regex': rf'{criterion.value}'})
    # Add more conditions as needed

    # Return the queryset unmodified if no matching condition was found
    return queryset

def filter_sections_by_logic(candidate_sections, token_search_inputs: List[TokenSearchInput]):
    # Filter the candidate sections based on the logical criteria contained within the TokenSearchInput instances
    for token_search_input in token_search_inputs:
        # Directly pass the TokenSearchInput instance to the apply_criterion function
        candidate_sections = apply_criterion(candidate_sections, token_search_input)
    
    # Assuming candidate_sections is a Django queryset, this will remove duplicates
    return candidate_sections.distinct()

def apply_distance_constraints(anchors, candidate_sections, distance_constraints):
    # Prepare a list to aggregate results
    aggregated_results = []

    for section in candidate_sections:
        for anchor_token in anchors:
            # Apply distance constraints for each anchor within the section
            tokens_within_distance = Token.objects.none()  # Start with an empty queryset

            if distance_constraints.type == 'both':
                tokens_within_distance = Token.objects.filter(
                    number__gte=anchor_token.number - distance_constraints.distance,
                    number__lte=anchor_token.number + distance_constraints.distance,
                    sectiontoken__section=section
                ).exclude(id=anchor_token.id)
            elif distance_constraints.type == 'before':
                tokens_within_distance = Token.objects.filter(
                    number__lte=anchor_token.number,
                    number__gt=anchor_token.number - distance_constraints.distance,
                    sectiontoken__section=section
                ).exclude(id=anchor_token.id)
            elif distance_constraints.type == 'after':
                tokens_within_distance = Token.objects.filter(
                    number__gte=anchor_token.number,
                    number__lt=anchor_token.number + distance_constraints.distance,
                    sectiontoken__section=section
                ).exclude(id=anchor_token.id)
            
            # Add the results to the aggregated list, taking care to remove duplicates
            for token in tokens_within_distance:
                if token not in aggregated_results:
                    aggregated_results.append(token)
    
    return aggregated_results


def process_search_inputs(token_search_inputs: List[TokenSearchInput]):
    # Step 1: Retrieve initial anchors for the first TokenSearchInput
    initial_anchors = retrieve_initial_anchors(token_search_inputs[0])
    
    # Step 2: Identify corresponding sections for the initial anchors
    candidate_sections = identify_candidate_sections(initial_anchors)
    
    # Step 3 and Step 4: Process subsequent criteria
    for criterion in token_search_inputs[1:]:
        # Apply logical "AND" and "NOT" criteria to the sections
        candidate_sections = filter_sections_by_logic(candidate_sections, criterion)

        # If the criterion includes distance constraints, apply them
        if criterion.distance:
            for anchor in initial_anchors:
                # Apply distance constraints here and update candidate_sections if necessary
                # This will filter the tokens based on distance from the anchor
                candidate_sections = apply_distance_constraints(anchor, candidate_sections, criterion.distance)

    # At this point, candidate_sections contains sections that match all criteria
    return candidate_sections
