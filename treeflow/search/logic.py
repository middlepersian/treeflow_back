from typing import Dict, List
from django.db.models import F
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
        tokens = retrieve_tokens(token_search_input)
        sections = identify_sections(list(tokens))

        if token_search_input["logical_operator"] == "AND":
            candidate_sections &= sections
        else:  # OR
            candidate_sections |= sections

    return candidate_sections


def filter_sections_by_distance(
    anchors, candidate_sections: List, token_search_inputs: List[Dict]
):
    """
    Filter sections by distance.
    """
    filtered_sections = set()

    for token_search_input in token_search_inputs:
        distance_type = token_search_input["distance_type"]
        distance = token_search_input["distance"]

        if distance == 0:
            return candidate_sections

        for section in candidate_sections:
            for anchor in anchors:
                if distance_type == "both":
                    tokens = section.tokens.filter(
                        number__gte=anchor.number - distance,
                        number__lte=anchor.number + distance,
                    ).exclude(id=anchor.id)
                elif distance_type == "before":
                    tokens = section.tokens.filter(
                        number__gte=anchor.number - distance,
                        number__lt=anchor.number,
                    ).exclude(id=anchor.id)
                elif distance_type == "after":
                    tokens = section.tokens.filter(
                        number__gt=anchor.number,
                        number__lte=anchor.number + distance,
                    ).exclude(id=anchor.id)

                if tokens.exists():
                    filtered_sections.add(section)

    return filtered_sections


def get_results(criteria: List):
    anchor = criteria[0]
    tokens = retrieve_tokens(anchor)
    sections = identify_sections(tokens)

    if "logical_operator" in anchor:
        sections = filter_sections_by_logic(sections, criteria[1:])
    elif "distance" in anchor:
        sections = filter_sections_by_distance(tokens, sections, criteria[1:])

    return sections
