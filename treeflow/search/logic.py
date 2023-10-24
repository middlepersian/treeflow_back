from django.db.models import Count, Q
from typing import List, Dict
from django.db.models import Subquery, OuterRef, Max, F, query, Q, Count, Exists
from treeflow.corpus.models import Section, Token, SectionToken
from treeflow.corpus.types.token import TokenSearchInput
import logging

logger = logging.getLogger(__name__)


def get_sections_with_highlighted_tokens(criteria_list: List[Dict[str, Dict[str, str]]], section_type: str) -> List[Dict]:

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
                    Token.objects.filter(sectiontoken__section=section, **
                                         {f"{field}__{search_method}": search_data["value"]})
                )
        results.append({
            'section': section,
            'highlighted_tokens': list(highlighted_tokens)
        })

    return results

def get_sections_with_positional_highlighted_tokens(criteria_list: List[TokenSearchInput], section_type: str) -> List[Dict]:
    logger.debug(f"Criteria list: {criteria_list}")

    # Base Q object for the section type
    section_query = Q(type=section_type)

    # Start with all sections of the given type
    filtered_sections = Section.objects.filter(section_query)

    # Begin with the first criteria
    first_criteria = criteria_list[0]
    field_filter = f'token__{first_criteria.field}'
    subquery = SectionToken.objects.filter(
        section=OuterRef('pk'),
        **{field_filter: first_criteria.value}
    )
    filtered_sections = filtered_sections.filter(Exists(subquery))

    # For each subsequent criteria, add another condition for its presence and position
    for i in range(1, len(criteria_list)):
        criteria = criteria_list[i]
        distance = criteria.distance_from_previous.distance if criteria.distance_from_previous else None
        field_filter = f'token__{criteria.field}'

        subquery = SectionToken.objects.filter(
            section=OuterRef('pk'),
            **{field_filter: criteria.value},
            token__number=Subquery(
                SectionToken.objects.filter(
                    section=OuterRef('section'),
                    token__transcription=criteria_list[i-1].value
                ).values('token__number')[:1]
            ) + distance
        )

        filtered_sections = filtered_sections.filter(Exists(subquery))

    logger.debug(f"Filtered sections query: {filtered_sections.query}")

    # Fetch the matching sections
    sections = list(filtered_sections)
    logger.debug(f"Sections matching criteria: {[s.id for s in sections]}")  # Log section IDs for brevity

    results = []
    for section in sections:
        highlighted_tokens = []
        for criteria in criteria_list:
            matching_tokens = Token.objects.filter(sectiontoken__section=section, **{criteria.field: criteria.value})
            highlighted_tokens.extend(matching_tokens)
            logger.debug(f"Matching tokens for section {section.id}: {[t.transcription for t in matching_tokens]}")  # Log token IDs for brevity
        results.append({
            'section': section,
            'highlighted_tokens': list(highlighted_tokens)
        })

    return results




def get_sections_by_multiple_token_criteria(section_criteria: Dict[str, str], token_criteria_list: List[Dict[str, Dict[str, str]]]) -> List[Section]:

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
