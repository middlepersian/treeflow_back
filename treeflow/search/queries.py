from django.db.models import Q, Subquery, OuterRef, Max, F
from typing import List, Dict, Tuple
from treeflow.corpus.models import Token, Section, SectionToken, POS
from treeflow.dict.models import Lemma

import logging
# create logger

logger = logging.getLogger('test')

def build_query_from_criteria(criteria: Dict) -> Q:
    """
    Convert a single criteria into a Q object for querying.
    """
    field = criteria["field"]
    value = criteria["value"]
    
    # Handle related fields
    if '__' in field:
        return Q(**{field: value})
    else:
        return Q(**{f'tokens__{field}': value})


def get_sections_matching_criteria(token_criteria: Dict, section_type: str) -> List[Section]:
    """
    Get sections that match the given criteria.
    """
    query = build_query_from_criteria(token_criteria)
    return Section.objects.filter(query, type=section_type)

def get_tokens_for_distance(token_criteria: Dict, matching_sections: List[Section], prev_token_number: int, enforce_order: bool) -> Tuple[List[Token], int]:
    """
    Get tokens for the distance search mode.
    """
    distance_criteria = token_criteria.get("min_previous_distance", {})
    distance = distance_criteria.get("distance_from_previous", 0)
    exact = distance_criteria.get("exact", False)
    
    expected_number_min = prev_token_number + distance
    expected_number_max = expected_number_min if exact else matching_sections.aggregate(
        Max('tokens__number'))['tokens__number__max']
    
    query = build_query_from_criteria(token_criteria)
    
    # Filter tokens based on their associated sections using the reverse relationship through the SectionToken model.
    tokens_for_distance = Token.objects.filter(query).filter(section_tokens__section__in=matching_sections)
    
    if enforce_order:
        query &= Q(number=prev_token_number + 1)
    else:
        query &= Q(number__gte=expected_number_min, number__lte=expected_number_max)

    tokens_for_distance = tokens_for_distance.filter(query)
    
    if tokens_for_distance:
        prev_token_number = tokens_for_distance.first().number
    else:
        return [], 0

    return tokens_for_distance, prev_token_number


def find_sections_with_tokens_logic_refactored(token_search_criteria: List[Dict], section_type: str, search_mode: str = "sequence", enforce_order: bool = False) -> List[Section]:
    initial_token = token_search_criteria[0]
    matching_sections = get_sections_matching_criteria(initial_token, section_type)
    
    prev_token_ids = Token.objects.filter(
        build_query_from_criteria(initial_token), sectiontoken__section__in=matching_sections
    ).values_list('id', flat=True)
    
    if search_mode == "sequence":
        for token_criteria in token_search_criteria[1:]:
            tokens = Token.objects.filter(
                build_query_from_criteria(token_criteria), sectiontoken__section__in=matching_sections
            ).annotate(prev_token_id=Subquery(
                Token.objects.filter(
                    sectiontoken__section__in=matching_sections,
                    id__in=prev_token_ids
                ).values('id')[:1]
            )).filter(number__gt=F('prev_token_id'))
            prev_token_ids = tokens.values_list('id', flat=True)
    elif search_mode == "distance":
        token_for_distance = Token.objects.filter(
            build_query_from_criteria(initial_token), sectiontoken__section__in=matching_sections
        ).first()
        if not token_for_distance:
            return []
        
        prev_token_number = token_for_distance.number
        
        for token_criteria in token_search_criteria[1:]:
            tokens_for_distance, prev_token_number = get_tokens_for_distance(token_criteria, matching_sections, prev_token_number, enforce_order)
            if not tokens_for_distance:
                return []
            
            initial_token = token_criteria
    
    # Fetch the sections and tokens in bulk
    sections_in_bulk = matching_sections.in_bulk()
    tokens_in_bulk = Token.objects.filter(id__in=prev_token_ids).in_bulk()

    results = []
    for section_id, section in sections_in_bulk.items():
        token_ids_for_section = [
            token_id for token_id, token in tokens_in_bulk.items()
            if any(build_query_from_criteria(criteria).children[0] in [(f'tokens__{k}', v) for k, v in token.__dict__.items()] for criteria in token_search_criteria)]
        matching_tokens = [tokens_in_bulk[token_id] for token_id in token_ids_for_section]
        results.append({
            'section': section,
            'tokens': matching_tokens
        })

    return results
