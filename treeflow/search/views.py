import logging
import time
from typing import Dict, List, Union

from django.core.paginator import Page, Paginator
from django.db.models import Prefetch, Q, QuerySet
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from treeflow.corpus.models import Section, SectionToken, Text

from .forms import LogicalFormSet, ResultFilterForm
from .models import SearchCriteria

logger = logging.getLogger(__name__)

queries = list()

@require_GET
def search_page(request):
    """
    Render the search page with the appropriate form and layout selection.
    """
    layout_selection = request.GET.get("layout_selection", "logical")
    # filter_form = ResultFilterForm()
    queryset = SearchCriteria.objects.none()
    formset_class = LogicalFormSet
    formset = formset_class(queryset=queryset)

    context = {
        # "filter_form": filter_form,
        "formset": formset,
        "layout_selection": layout_selection,
        "results": Section.objects.none(),
    }

    if request.headers.get("HX-Request"):
        return render(request, "search/_partial.html", context)

    return render(request, "pages/search.html", context)

def results_view(request):
    """
    Handle search results display based on GET or POST requests.
    """
    page_number = request.GET.get("page", 1)
    results = None
    # text_id = request.GET.get("text", "")
    # section_id = request.GET.get("section", "")

    # text = get_object_or_404(Text, id=text_id) if text_id else None
    # section = get_object_or_404(Section, id=section_id) if section_id else None
    # filter_form = ResultFilterForm(initial={"text": text, "section": section})

    try:
        # if request.method == "POST":
        results = handle_request(request)

        # Request method of next page is GET; GET takes all sections..
        # elif request.method == "GET":
            # queries = request.GET.getlist("query", [])
            # logger.debug(f"Queries (GET): {queries}")
            # results = SectionToken.objects.filter()  # Start with all sections
            # if text_id or section_id:
            #     logger.debug(f"Text ID: {text_id}, Section ID: {section_id}")
            #     results = narrow_results(results, text_id, section_id)

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        results = Section.objects.none()

    # Ensure results is a queryset before prefetching
    if not isinstance(results, QuerySet):
        results = Section.objects.filter(id__in=[r.id for r in results])

    results.prefetch_related("section__tokens")
    paginator = Paginator(results, 10)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "search/results.html",
        {
            "page_obj": page_obj,
            "queries": queries,
        },
    )

def handle_request(request) -> QuerySet:
    """
    Handle form submission for search results.
    """
    # layout_selection = request.POST.get("layout_selection", "logical")
    formset_class = LogicalFormSet
    formset = formset_class(request.GET)

    if formset.is_valid():
        logger.debug("Formset is valid.")
        data = [f for f in formset.cleaned_data if f]
        # MARK: - data
        results = get_results(data)
        logger.debug(f"Found {len(results)} results.")
    else: # TODO Formset on next Page invalid --> No proper querying/filtering?
        logger.error("Formset is invalid.")
        results = Section.objects.none()
    return results

def get_results(criteria: List) -> QuerySet:
    """
    Retrieve search results based on given criteria.
    """
    start_time = time.time()
    if not criteria:
        logger.error("No criteria provided")
        return Section.objects.none()

    for form in criteria:
            queries.append(form["query"])
    anchor_criterion = criteria[0]
    filters = criteria[1:]
    anchor_tokens = retrieve_tokens(anchor_criterion)
    sections = identify_sections(anchor_tokens)

    if filters:
        if "logical_operator" in anchor_criterion:
            sections = filter_sections_by_logic(sections, filters)
        # elif "distance" in anchor_criterion:
        #     sections = filter_sections_by_distance(anchor_tokens, sections, filters)

    end_time = time.time()
    logger.info(f"Total time taken in get_results: {end_time - start_time:.4f} seconds")

    return sections

def retrieve_tokens(criteria: Dict) -> QuerySet:
    """
    Retrieve SectionTokens based on the search criteria.
    """
    value = criteria.pop("query", None)
    query_field = criteria.pop("query_field", "")
    query_type = criteria.pop("query_type", "contains")
    case_sensitive = criteria.pop("case_sensitive", False)
    case_insensitive_prefix = "" if case_sensitive else "i"

    if not value or not query_field:
        return SectionToken.objects.none()

    query_lookup = {
        "exact": f"token__{query_field}__{case_insensitive_prefix}exact",
        "prefix": f"token__{query_field}__{case_insensitive_prefix}startswith",
        "suffix": f"token__{query_field}__{case_insensitive_prefix}endswith",
        "regex": f"token__{query_field}__{case_insensitive_prefix}regex",
        "contains": f"token__{query_field}__{case_insensitive_prefix}contains",
    }

    query = Q(**{query_lookup.get(query_type, query_lookup["contains"]): value})

    for k, v in criteria.items():
        if v and not any(x in k for x in ["logical", "distance", "id"]):
            query &= Q(**{k: v})

    return SectionToken.objects.filter(query).prefetch_related("token", "section")

def identify_sections(tokens: QuerySet) -> QuerySet:
    """
    Identify sections related to a list of SectionTokens.
    """
    token_ids = tokens.values_list('id', flat=True)
    return Section.objects.filter(sectiontoken__id__in=token_ids, type="sentence").distinct()

def filter_sections_by_logic(candidate_sections: QuerySet, token_search_inputs: List[Dict]) -> QuerySet:
    """
    Filter sections based on logical operators (AND/OR).
    """
    for token_search_input in token_search_inputs:
        filter_tokens = retrieve_tokens(token_search_input)
        filter_sections = identify_sections(filter_tokens)

        if token_search_input.get("logical_operator") == "AND":
            candidate_sections = candidate_sections.filter(id__in=filter_sections.values_list("id", flat=True))
        else:  # OR
            candidate_sections |= filter_sections

    return candidate_sections

# def filter_sections_by_distance(
#     anchor_tokens: List[Token],
#     candidate_sections: List[Section],
#     token_search_inputs: List[Dict],
# ) -> List[Section]:
#     """
#     Filter sections by distance.
#     """

#     section_ids = []

#     for token_search_input in token_search_inputs:
#         filter_tokens = retrieve_tokens(token_search_input)
#         filter_sections = identify_sections(filter_tokens)
#         candidate_sections &= filter_sections
#         ids = [token.id for token in filter_tokens]

#         distance = token_search_input["distance"]
#         distance_type = token_search_input["distance_type"]

#         for section in candidate_sections:
#             q_objects = Q()

#             for anchor in anchor_tokens:
#                 if distance_type == "both":
#                     q_objects |= Q(number__range=(anchor.number - distance, anchor.number + distance))
#                 elif distance_type == "before":
#                     q_objects |= Q(number__range=(anchor.number - distance, anchor.number))
#                 elif distance_type == "after":
#                     q_objects |= Q(number__range=(anchor.number, anchor.number + distance))

#             tokens = section.tokens.filter(q_objects, id__in=ids)

#             if tokens:
#                 section_ids.append(section.id)

#     sections = Section.objects.filter(id__in=section_ids)

#     return sections

# def narrow_results(results: QuerySet, text_id=None, section_id=None) -> QuerySet:
#     """
#     Narrow down results based on text and section IDs.
#     """
#     query = Q()
#     if text_id:
#         query &= Q(text_id=text_id)
#     if section_id:
#         query &= Q(id=section_id)
#     return results.filter(query)