from typing import List, Dict
from django.db.models import Subquery, OuterRef, Max, F, query, Q
from treeflow.corpus.models import Section, Token, SectionToken
import logging

logger = logging.getLogger(__name__)

def get_sections_with_token(token_value: str, section_type: str) -> List[Section]:
    sections = Section.objects.filter(
        type=section_type,
        tokens__transcription=token_value
    ).distinct()
    return sections


def get_sections_with_token_position(token_value: str, section_type: str) -> List[Section]:
    sections = Section.objects.filter(
        type=section_type,
        tokens__transcription=token_value
    ).annotate(
        token_position=F('sectiontoken__token__number')
    ).filter(
        sectiontoken__token__transcription=token_value
    ).distinct()

    return sections



def find_tokens_within_sections(
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

    if search_mode == "all":
        return find_sections_with_all_tokens(token_search_criteria, section_type)
    
    if search_mode == "sequence":
        return find_sections_with_ordered_tokens(token_search_criteria, section_type)

    elif search_mode == "distance":
        return find_sections_by_token_distance(token_search_criteria, section_type, enforce_order)

    logger.info('Exiting find_sections_with_tokens_logic function')

def find_sections_with_all_tokens(token_search_criteria: List[Dict], section_type: str) -> List[Section]:
    """
    Find sections containing all the specified tokens, without considering the order of tokens.
    """
    initial_token = token_search_criteria[0]
    logger.debug(f'Initial token: {initial_token}')
    
    # Start with sections containing the first token
    matching_sections = Section.objects.filter(
        **{f'tokens__{initial_token["field"]}': initial_token["value"], 'type': section_type})
    logger.debug(f'Matching sections after initial filter: {matching_sections.query}')

    for token_criteria in token_search_criteria[1:]:
        # Filter sections based on the presence of the token, without considering its position
        matching_sections = matching_sections.filter(
            **{f'sectiontoken__token__{token_criteria["field"]}': token_criteria["value"]}
        )
        logger.debug(f'Matching sections after token filter: {matching_sections.query}')

    return list(matching_sections)

def find_sections_with_ordered_tokens(token_search_criteria: List[Dict], section_type: str, enforce_order: bool) -> List[Section]:
    # Start with all sections containing the first token
    valid_sections = Section.objects.filter(
        type=section_type,
        **{f'tokens__{token_search_criteria[0]["field"]}': token_search_criteria[0]["value"]}
    )
    logger.debug(f"Sections after {token_search_criteria[0]['value']} filter: {valid_sections.query}")

    # Annotate the valid_sections with the position of each token in the section's token list
    for idx, token_criteria in enumerate(token_search_criteria[1:], start=1):
        subquery = SectionToken.objects.filter(
            section=OuterRef('pk'),
            token__transcription=token_criteria["value"]
        ).values('token__number')

        # Annotate with the position of each token
        valid_sections = valid_sections.annotate(**{f'token_pos_{idx}': Subquery(subquery[:1])})

    # Filter to ensure each token's position is greater than the previous token's position
    if enforce_order:
        for idx in range(2, len(token_search_criteria) + 1):
            valid_sections = valid_sections.filter(**{f'tokens__number__exact': F(f'token_pos_{idx - 1}')})

    logger.debug(f"Sections after position filter: {valid_sections.query}")

    # At this point, valid_sections should contain sections that have all the tokens in the correct order
    # Filter out any sections that didn't have all tokens annotated (i.e., one or more tokens were missing)
    valid_sections = valid_sections.exclude(**{f'tokens__number__exact': len(token_search_criteria)})

    logger.debug(f"Final matching sections: {valid_sections.query}")
    return list(valid_sections)

def find_sections_by_token_distance(token_search_criteria: List[Dict], section_type: str, enforce_order: bool) -> List[Section]:

    # Starting with the first token in the search criteria
    initial_token = token_search_criteria[0]
    logger.debug(f'Initial token: {initial_token}')
    
    matching_sections = Section.objects.filter(
        **{f'tokens__{initial_token["field"]}': initial_token["value"], 'type': section_type})
    logger.debug(f'Matching sections after initial filter: {matching_sections.query}')

    for token_criteria in token_search_criteria[1:]:
        logger.debug(f"Starting iteration with token: {initial_token['value']}")
        
        updated_matching_sections = []
        
        # Iterate over the current matching sections to get the token number of the initial_token for each section
        for section in matching_sections:
            logger.debug(f"Evaluating section ID: {section.id}")
            section_token = SectionToken.objects.filter(
                section=section, 
                token__transcription=initial_token["value"]
            ).first()
            
            if section_token:
                prev_token_number = section_token.token.number
            else:
                logger.warning(f"Token {initial_token['value']} not found in section ID: {section.id}")
                continue
            
            # Filter sections based on the token number and criteria
            if "min_previous_distance" in token_criteria:
                distance = token_criteria["min_previous_distance"]["distance_from_previous"] or 0
                exact = token_criteria["min_previous_distance"]["exact"] or False
                if exact:
                    expected_number_min = prev_token_number + distance
                    expected_number_max = expected_number_min
                else:
                    expected_number_min = prev_token_number + distance
                    expected_number_max = prev_token_number + distance + 1

                # If enforce_order is True, ensure token order by making sure the next token's number is greater than the previous token's number
                if enforce_order:
                    filtered_sections = Section.objects.filter(id=section.id, tokens__number=prev_token_number + 1)
                else:
                    filtered_sections = Section.objects.filter(id=section.id, tokens__number__gte=expected_number_min, tokens__number__lte=expected_number_max)
                
                if filtered_sections.exists():
                    updated_matching_sections.extend(list(filtered_sections))
            
            matching_sections = updated_matching_sections

        if not matching_sections:
            raise ValueError("No matching sections found for the given token sequence.")
        
        # Update initial token for next iteration
        initial_token = token_criteria

    return list(set(matching_sections))
