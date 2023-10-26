from typing import List, Dict
from django.core.exceptions import EmptyResultSet
from django.db.models import Subquery, OuterRef, Max, F, query, Q, Count, Exists
from treeflow.corpus.models import Section, Token, SectionToken
from treeflow.corpus.types.token import TokenSearchInput
from treeflow.corpus.types.text import Text
from strawberry import relay

import logging

logger = logging.getLogger(__name__)


def search_tokens(criteria_list: List[TokenSearchInput], section_type: str, texts: List[str] = None) -> List[Dict]:
    logger.debug(f"#############################################")
    logger.debug(
        f"search_tokens (criteria_list: {criteria_list}, section_type: {section_type})")

    # Base Q object for the section type
    query = Q(type=section_type)

    #Filter by Text
    if texts:
        query &= Q(text__id__in=texts)
        logger.debug(f"Filtering by texts: {texts}")

    section_ids_list = []

    for idx, token_criteria in enumerate(criteria_list):
        logger.debug(f"Processing token_criteria {idx + 1}: {token_criteria}")
        token_query = Q()

        field = token_criteria.field
        value = token_criteria.value
        # default to exact if not specified
        method = getattr(token_criteria, "query_type", "exact")

        if value:
            token_query &= Q(**{f"tokens__{field}__{method}": value})

        if token_criteria.pos_token:
            for pos in token_criteria.pos_token:
                token_query &= Q(tokens__pos_token__pos=pos.pos)

        if token_criteria.feature_token:
            for feature in token_criteria.feature_token:
                token_query &= Q(tokens__feature_token__feature=feature.feature,
                                 tokens__feature_token__feature_value=feature.feature_value)

        if token_criteria.stopwords:
            # Assuming you have a list of stopwords
            token_query &= ~Q(tokens__transcription__in=STOPWORDS_LIST)

        logger.debug(
            f"Constructed token_query for criteria {idx + 1}: {token_query}")

        section_ids = Section.objects.filter(
            query & token_query).values_list('id', flat=True)
        logger.debug(
            f"Sections matching criteria {idx + 1}: {Section.objects.filter(query & token_query).query}")
        logger.debug(
            f"Number of sections found for criteria {idx + 1}: {len(section_ids)}")

        section_ids_list.append(set(section_ids))

    try:
        final_section_ids = set.intersection(*section_ids_list)
        logger.debug(f"Final intersected section IDs: {final_section_ids}")

        sections = Section.objects.filter(id__in=final_section_ids).distinct()
        logger.debug(
            f"Number of sections after intersection: {sections.count()}")
        logger.debug(f"Sections matching final criteria: {sections.query}")

    except EmptyResultSet:
        return []

    results = []
    for section in sections:
        highlighted_tokens_set = set()  # Using a set to ensure uniqueness
        for token_criteria in criteria_list:
            field = token_criteria.field
            value = token_criteria.value
            search_method = getattr(token_criteria, "query_type", "icontains")

            # Base query for tokens in the current section
            query = Token.objects.filter(sectiontoken__section=section)

            # Modify the query based on the criteria
            if field and value:
                query = query.filter(**{f"{field}__{search_method}": value})
            if token_criteria.pos_token:
                # Assuming only one POS criteria for simplicity
                pos = token_criteria.pos_token[0].pos
                query = query.filter(pos_token__pos=pos)
            if token_criteria.feature_token:
                feature = token_criteria.feature_token[0].feature
                feature_value = token_criteria.feature_token[0].feature_value
                query = query.filter(
                    feature_token__feature=feature, feature_token__feature_value=feature_value)

            highlighted_tokens_set.update(query)

        logger.debug(
            f"Number of highlighted tokens for section {section.id}: {len(highlighted_tokens_set)}")
        results.append({
            'section': section,
            'highlighted_tokens': list(highlighted_tokens_set)
        })

    return results


def search_tokens_by_position(criteria_list: List[TokenSearchInput], section_type: str) -> List[Dict]:
    logger.debug(f"#############################################")
    logger.debug(
        f"search_tokens_by_position (criteria_list: {criteria_list}, section_type: {section_type})")


    # Base Q object for the section type
    query = Q(type=section_type)#
    # Filter by Text
    if texts:
        query &= Q(text__id__in=texts)
        logger.debug(f"Filtering by texts: {texts}")


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
    # Log section IDs for brevity
    logger.debug(f"Sections matching criteria: {[s.id for s in sections]}")

    results = []
    for section in sections:
        highlighted_tokens = []
        for criteria in criteria_list:
            matching_tokens = Token.objects.filter(
                sectiontoken__section=section, **{criteria.field: criteria.value})
            highlighted_tokens.extend(matching_tokens)
            # Log token IDs for brevity
            logger.debug(
                f"Matching tokens for section {section.id}: {[t.transcription for t in matching_tokens]}")
        results.append({
            'section': section,
            'highlighted_tokens': list(highlighted_tokens)
        })

    return results
