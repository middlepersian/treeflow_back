from typing import List, Dict
from django.db.models import Subquery, OuterRef, Max, F, query, Q, Count
from treeflow.corpus.models import Section, Token, SectionToken
import logging

logger = logging.getLogger(__name__)

def get_sections_with_highlighted_tokens(criteria: Dict[str, Dict[str, str]], section_type: str) -> List[Dict]:
    """
    Fetch sections based on the specified criteria and get highlighted tokens within them.
    
    Args:
    - criteria (dict): A dictionary where keys are the token fields (e.g., 'tokens__transcription', 'tokens__transliteration') 
      and values are dictionaries specifying the value and method for searching in those fields.
    - section_type (str): The type of section to filter by.
    
    Returns:
    - List[Dict]: List of dictionaries, each containing a section and its corresponding highlighted tokens.
    """

    # Start with a base Q object to accumulate our queries
    query = Q(type=section_type)

    # Build the query based on the provided criteria
    for field, search_data in criteria.items():
        search_method = search_data.get("method", "exact")  # Default to 'exact' if not specified
        query &= Q(**{f"{field}__{search_method}": search_data["value"]})

    # Query the sections based on the criteria
    sections = Section.objects.filter(query).distinct()
    logger.debug(f"Sections matching criteria: {sections.query}")

    results = []
    
    # For each section, fetch the tokens that match the search criteria and store them.
    for section in sections:
        matching_tokens = Token.objects.filter(sectiontoken__section=section, **{f"{field.split('__')[1]}__{search_method}": search_data["value"]})
        logger.debug(f"Matching tokens: {matching_tokens.query}")
        
        # Append the section and its highlighted tokens to the results list
        results.append({
            'section': section,
            'highlighted_tokens': list(matching_tokens)
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

def find_sections_with_ordered_tokens(token_dicts):
    tokens = [t['value'] for t in token_dicts]
    valid_sections = set(SectionToken.objects.filter(token__transcription=tokens[0]).values_list('section', flat=True))
    logger.debug(f"Initial sections containing '{tokens[0]}': {valid_sections}")

    for idx, token_value in enumerate(tokens[1:], start=1):
        for section in list(valid_sections):
            prev_token = Token.objects.filter(transcription=tokens[idx - 1], section_tokens=section).first()
            curr_token = Token.objects.filter(transcription=token_value, section_tokens=section).first()
            
            if not prev_token or not curr_token:
                valid_sections.remove(section)
                continue

            prev_token_number = prev_token.number
            curr_token_number = curr_token.number
            
            logger.debug(f"For section {section}, '{tokens[idx - 1]}' position: {prev_token_number}, '{token_value}' position: {curr_token_number}")
            
            if prev_token_number >= curr_token_number or Token.objects.filter(
                transcription__in=tokens[idx - 1: idx], 
                section_tokens=section,
                number__gt=prev_token_number,
                number__lt=curr_token_number
            ).exists():
                valid_sections.remove(section)
        
        logger.debug(f"Remaining valid sections after filtering by '{token_value}': {valid_sections}")

    logger.debug(f"Final valid sections after processing all tokens: {valid_sections}")
    return valid_sections


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

