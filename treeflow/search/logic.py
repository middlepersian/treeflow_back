from typing import List, Dict
from django.db.models import Subquery, OuterRef, Max, F, query, Q, Count
from treeflow.corpus.models import Section, Token, SectionToken
import logging

logger = logging.getLogger(__name__)


from django.db.models import Count, Q

def get_sections_with_highlighted_tokens(criteria_list: List[Dict[str, Dict[str, str]]], section_type: str) -> List[Dict]:
    """
    ... [rest of the docstring]
    """
    
    # Base Q object for the section type
    section_query = Q(type=section_type)

    # Start by annotating the count of tokens that match each criterion
    annotations = {}
    for index, criteria in enumerate(criteria_list):
        token_query = Q()
        for field, search_data in criteria.items():
            search_method = search_data.get("method", "exact")
            token_query &= Q(**{f"tokens__{field}__{search_method}": search_data["value"]})
        annotation_name = f"token_match_{index}"
        annotations[annotation_name] = Count('tokens', filter=token_query, distinct=True)
    
    # Filter sections where each annotation count is at least 1 (indicating a match for each criterion)
    filtered_sections = Section.objects.filter(section_query).annotate(**annotations)
    for index, _ in enumerate(criteria_list):
        filtered_sections = filtered_sections.filter(**{f"token_match_{index}__gte": 1})

    # Fetch the matching sections
    sections = list(filtered_sections)

    results = []
    for section in sections:
        highlighted_tokens = []
        for criteria in criteria_list:
            for field, search_data in criteria.items():
                search_method = search_data.get("method", "exact")
                highlighted_tokens.extend(
                    Token.objects.filter(sectiontoken__section=section, **{f"{field}__{search_method}": search_data["value"]})
                )
        results.append({
            'section': section,
            'highlighted_tokens': list(highlighted_tokens)
        })

    return results


def get_sections_by_multiple_token_criteria(section_criteria: Dict[str, str], token_criteria_list: List[Dict[str, Dict[str, str]]]) -> List[Section]:
    """
    ... [rest of the docstring remains unchanged]
    """
    query = Q()
    for field, value in section_criteria.items():
        query &= Q(**{field: value})

    section_ids_list = []

    for token_criteria in token_criteria_list:
        token_query = Q()
        for field, search_data in token_criteria.items():
            value = search_data["value"]
            method = search_data.get("method", "icontains")  # default to icontains if not specified
            token_query &= Q(**{f"tokens__{field}__{method}": value})

        section_ids = Section.objects.filter(query & token_query).values_list('id', flat=True)
        section_ids_list.append(set(section_ids))

    final_section_ids = set.intersection(*section_ids_list)
    sections = Section.objects.filter(id__in=final_section_ids).distinct()
    logger.debug(f"Sections matching criteria: {sections.query}")

    return sections
