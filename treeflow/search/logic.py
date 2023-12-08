from typing import Dict, List
from django.db.models import Q
from treeflow.corpus.models import Section, Token


def retrieve_tokens(criteria: Dict) -> List[Token]:
    """
    Retrieve all tokens that match the given criteria.
    These tokens will act as potential anchors for further search.

    :param criteria: The anchor object containing the search criteria.
    :return: A list of Token objects that match the criteria.

    """

    tokens = Token.objects.none()

    if criteria["query_type"] == "exact":
        tokens = Token.objects.filter(
            **{f"{criteria['query_field']}__iexact": criteria["query"]}
        )
    elif criteria["query_type"] == "fuzzy":
        tokens = Token.objects.filter(
            **{f"{criteria['query_field']}__icontains": criteria["query"]}
        )

    # TODO: istartswith, regexp, fuzzy

    return tokens


def identify_sections(tokens: List[Token]) -> List[Section]:
    """
    Identify distinct sections from a list of anchor tokens.

    :param anchors: A list of Token objects to find the sections for.
    :return: A list of unique Section objects that are associated with the tokens.
    """

    sections = Section.objects.none()
    section_ids = set()

    for token in tokens:
        section_tokens = token.sectiontoken_set.all()
        for section_token in section_tokens:
            section_ids.add(section_token.section_id)

    sections = Section.objects.filter(id__in=section_ids, type="sentence")

    return sections


def filter_sections_by_logic(
    candidate_sections: List[Section], token_search_inputs: List[Dict]
) -> List[Section]:
    """
    Filter sections by logical operator.
    """

    for token_search_input in token_search_inputs:
        filter_tokens = retrieve_tokens(token_search_input)
        filter_sections = identify_sections(filter_tokens)

        if token_search_input["logical_operator"] == "AND":
            candidate_sections &= filter_sections
        else:  # OR
            candidate_sections |= filter_sections

    return candidate_sections


def filter_sections_by_distance(
    anchor_tokens: List[Token],
    candidate_sections: List[Section],
    token_search_inputs: List[Dict],
) -> List[Section]:
    """
    Filter sections by distance.
    """

    filtered_sections = set()

    for token_search_input in token_search_inputs:
        filter_tokens = retrieve_tokens(token_search_input)
        filter_sections = identify_sections(filter_tokens)
        candidate_sections &= filter_sections
        ids = [token.id for token in filter_tokens]

        distance = token_search_input["distance"]
        distance_type = token_search_input["distance_type"]

        for section in candidate_sections:
            q_objects = Q()

            for anchor in anchor_tokens:
                if distance_type == "both":
                    q_objects |= Q(number__range=(anchor.number - distance, anchor.number + distance))
                elif distance_type == "before":
                    q_objects |= Q(number__range=(anchor.number - distance, anchor.number))
                elif distance_type == "after":
                    q_objects |= Q(number__range=(anchor.number, anchor.number + distance))

            tokens = section.tokens.filter(q_objects, id__in=ids)

            if tokens.exists():
                filtered_sections.add(section)

    return list(filtered_sections)

def get_results(criteria: List):
    anchor_criterium = criteria[0]
    filters = criteria[1:]
    anchor_tokens = retrieve_tokens(anchor_criterium)
    sections = identify_sections(anchor_tokens)

    if len(criteria) == 1:
        return sections
    elif "logical_operator" in anchor_criterium:
        sections = filter_sections_by_logic(sections, filters)
    elif "distance" in anchor_criterium:
        sections = filter_sections_by_distance(anchor_tokens, sections, filters)

    return sections
