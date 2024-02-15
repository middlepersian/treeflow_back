import logging
import time
from django.core.paginator import Paginator
from typing import Dict, List
from django.db.models import Q
from uuid import UUID
from treeflow.corpus.models import Section, Token

logger = logging.getLogger(__name__)


def retrieve_tokens(criteria: Dict, page_size=1000) -> List[Token]:
    """
    Retrieve all tokens that match the given criteria in batches.
    These tokens will act as potential anchors for further search.

    :param criteria: The anchor object containing the search criteria.
    :param page_size: Number of tokens to retrieve per batch.
    :return: A list of Token objects that match the criteria.
    """

    filter_tmp = criteria.copy()

    value = filter_tmp.pop("query")
    query_field = filter_tmp.pop("query_field")
    query_type = filter_tmp.pop("query_type")
    i = "" if filter_tmp.pop("case_sensitive") else "i"

    # Build the query
    query = Q(**{f"{query_field}__{i}{query_type}": value})
    for k, v in filter_tmp.items():
        if v:
            query &= Q(**{k: v})

    tokens_queryset = Token.objects.filter(query).only('id').values_list('id', flat=True)
    #log the query
    logger.debug(tokens_queryset.query)
    paginator = Paginator(tokens_queryset, page_size)

    tokens = []
    for page_num in range(1, paginator.num_pages + 1):
        page = paginator.page(page_num)
        tokens.extend(list(page.object_list))

    logger.debug(f"Retrieved {len(tokens)} tokens in batches.")
    return tokens


def identify_sections(tokens: List[UUID], batch_size=1000) -> List[Section]:
    """
    Identify distinct sections from a list of anchor token UUIDs using batch processing.

    :param tokens: A list of Token UUIDs to find the sections for.
    :param batch_size: Number of token_ids to process per batch.
    :return: A list of unique Section objects that are associated with the tokens.
    """
    sections = []
    for i in range(0, len(tokens), batch_size):
        batch_token_ids = tokens[i:i + batch_size]

        batch_sections = Section.objects.filter(
            sectiontoken__token_id__in=batch_token_ids,
            type="sentence"
        ).prefetch_related(
            "sectiontoken_set",
            "sectiontoken_set__token"
        )

        sections.extend(list(batch_sections))

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

    section_ids = []

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

            if tokens:
                section_ids.append(section.id)

    sections = Section.objects.filter(id__in=section_ids)

    return sections


def get_results(criteria: List):
    start_time = time.time()

    anchor_criterium = criteria[0]
    filters = criteria[1:]
    anchor_tokens = retrieve_tokens(anchor_criterium)
    sections = identify_sections(anchor_tokens)

    if len(criteria) == 1:
        logger.debug("Only anchor token provided, returning sections.")
    elif "logical_operator" in anchor_criterium:
        sections = filter_sections_by_logic(sections, filters)
    elif "distance" in anchor_criterium:
        sections = filter_sections_by_distance(anchor_tokens, sections, filters)

    end_time = time.time()
    print(f"Total time taken in get_results: {end_time - start_time} seconds")
     

    return sections


def narrow_results(results: List, text: None, section: None):
    query = Q()

    if text: query.add(Q(text_id=text), Q.AND)
    if section: query.add(Q(id=section), Q.AND)

    filtered = results.filter(query)
    
    return filtered