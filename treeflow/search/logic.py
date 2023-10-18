from typing import List, Dict
from django.db.models import Subquery, OuterRef, Max
from treeflow.corpus.models import Section, Token, SectionToken
import logging

logger = logging.getLogger(__name__)

def find_sections_with_tokens_logic(
    token_search_criteria: List[Dict],
    section_type: str,
    search_mode: str = "sequence",
    enforce_order: bool = False
) -> List[Section]:

    logger.info('#############################################')


    logger.info('Entering find_sections_with_tokens_logic function')
    
    if not token_search_criteria or len(token_search_criteria) < 2:
        logger.warning('No token search criteria provided or less than two criteria provided')
        return []

    # Starting with the first token in the search criteria
    initial_token = token_search_criteria[0]
    logger.debug(f'Initial token: {initial_token}')
    
    matching_sections = Section.objects.filter(
        **{f'tokens__{initial_token["field"]}': initial_token["value"], 'type': section_type})
    logger.debug(f'Matching sections after initial filter: {matching_sections.query}')

    if search_mode == "sequence":
        for token_criteria in token_search_criteria[1:]:
            # Get the sections where this token appears after the previous token
            matching_sections = matching_sections.filter(
                **{f'sectiontoken__token__{token_criteria["field"]}': token_criteria["value"]},
                sectiontoken__token__number__gt=Subquery(
                    SectionToken.objects.filter(
                        section=OuterRef('pk'),
                        **{f'token__{initial_token["field"]}': initial_token["value"]}
                    ).values('token__number')[:1]
                )
            )
            logger.debug(f'Matching sections after sequence filter: {matching_sections.query}')
            initial_token = token_criteria

    elif search_mode == "distance":
        prev_token_number = Token.objects.filter(
            **{initial_token["field"]: initial_token["value"], 'section_tokens__in': matching_sections}).first().number

        for token_criteria in token_search_criteria[1:]:
            logger.debug(f"Starting iteration with token: {initial_token['value']} (number: {prev_token_number})")
            
            if "min_previous_distance" in token_criteria:
                distance = token_criteria["min_previous_distance"]["distance_from_previous"] or 0
                exact = token_criteria["min_previous_distance"]["exact"] or False
                if exact:
                    expected_number_min = prev_token_number + distance
                    expected_number_max = expected_number_min
                else:
                    expected_number_min = prev_token_number + distance
                    max_token_number_in_section = matching_sections.aggregate(
                        Max('tokens__number'))['tokens__number__max']
                    expected_number_max = expected_number_min + 1

            else:
                expected_number_min = prev_token_number + 1
                expected_number_max = prev_token_number + 1

            logger.debug(f"Expected token number range: {expected_number_min} - {expected_number_max}")

            # If enforce_order is True, ensure token order by making sure the next token's number is greater than the previous token's number
            if enforce_order:
                logger.debug(f'Enforcing order: {enforce_order}')
                matching_sections = matching_sections.filter(tokens__number=prev_token_number + 1)
            else:
                matching_sections = matching_sections.filter(
                    tokens__number__gte=expected_number_min, tokens__number__lte=expected_number_max)

            logger.debug(f"Number of matching sections after filtering: {matching_sections.count()}")

            if not matching_sections.exists():
                raise ValueError(
                    "No matching sections found for the given token sequence.")

            # Update previous token number for next iteration
            prev_token_number = Token.objects.filter(
                **{token_criteria["field"]: token_criteria["value"], 'section_tokens__in': matching_sections}).first().number

            logger.debug(f"Updated prev_token_number for next iteration: {prev_token_number}")

            # Update initial token for next iteration
            initial_token = token_criteria

    logger.info('Exiting find_sections_with_tokens_logic function')
    return list(matching_sections.distinct())

