from typing import List, Dict
from django.core.exceptions import EmptyResultSet
from django.db.models import Subquery, OuterRef, Max, F, query, Q, Count, Exists
from treeflow.corpus.models import Section, Token, SectionToken
from treeflow.corpus.types.token import TokenSearchInput
import logging

logger = logging.getLogger(__name__)


def search_tokens(criteria_list: List[TokenSearchInput], section_type: str) -> List[Dict]:
    logger.debug(f"#############################################")
    logger.debug(f"search_tokens (criteria_list: {criteria_list}, section_type: {section_type})")

    # Base Q object for the section type
    query = Q(type=section_type)

    section_ids_list = []

    for token_criteria in criteria_list:
        token_query = Q()

        field = token_criteria.field
        value = token_criteria.value
        method = getattr(token_criteria, "query_type", "exact")  # default to icontains if not specified
        token_query &= Q(**{f"tokens__{field}__{method}": value})
        section_ids = Section.objects.filter(query & token_query).values_list('id', flat=True)
        section_ids_list.append(set(section_ids))
    try:
        final_section_ids = set.intersection(*section_ids_list)
        sections = Section.objects.filter(id__in=final_section_ids).distinct()
        logger.debug(f"Sections matching criteria: {sections.query}")

    except EmptyResultSet:
        return []

    results = []
    for section in sections:
        highlighted_tokens = []
        for token_criteria in criteria_list:
            field = token_criteria.field
            value = token_criteria.value
            search_method = getattr(token_criteria, "query_type", "icontains")
            highlighted_tokens.extend(
                Token.objects.filter(sectiontoken__section=section, **
                                     {f"{field}__{search_method}": value})
            )
        results.append({
            'section': section,
            'highlighted_tokens': list(highlighted_tokens)
        })

    return results


def search_tokens_by_position(criteria_list: List[TokenSearchInput], section_type: str) -> List[Dict]:
    logger.debug(f"#############################################")
    logger.debug(f"search_tokens_by_position (criteria_list: {criteria_list}, section_type: {section_type})")

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

    subqueries = []

    for i in range(1, len(criteria_list)):
        criteria = criteria_list[i]
        distance = criteria.distance_from_previous.distance if criteria.distance_from_previous else 0
        exact = criteria.distance_from_previous.exact if criteria.distance_from_previous else True
        field_filter = f'token__{criteria.field}'

        # Adjust the token number condition based on the exact flag
        if exact:
            token_number_condition = Q(token__number=Subquery(
                SectionToken.objects.filter(
                    section=OuterRef('section'),
                    token__transcription=criteria_list[i-1].value
                ).values('token__number')[:1]
            ) + distance, **{field_filter: criteria.value})
        else:
            token_number_condition = Q(token__number__gte=Subquery(
                SectionToken.objects.filter(
                    section=OuterRef('section'),
                    token__transcription=criteria_list[i-1].value
                ).values('token__number')[:1]
            ) + distance, **{field_filter: criteria.value})

        subquery = SectionToken.objects.filter(
            section=OuterRef('pk')
        ).filter(token_number_condition)

        subqueries.append(subquery)

    for sq in subqueries:
        filtered_sections = filtered_sections.filter(Exists(sq))

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
            # Log token IDs for brevity
            logger.debug(f"Matching tokens for section {section.id}: {[t.transcription for t in matching_tokens]}")
        results.append({
            'section': section,
            'highlighted_tokens': list(highlighted_tokens)
        })

    return results
