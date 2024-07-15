import json
import logging
import time
from typing import Dict, List

from django.core.paginator import Paginator
from django.db.models import Q, QuerySet
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET

from treeflow.corpus.models import Section, SectionToken

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
        results = handle_request(request)
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

def handle_request(request: HttpRequest) -> QuerySet:
    """
    Handle form submission for search results.
    """
    # Retrieve layout selection and set formset class
    # layout_selection = request.POST.get("layout_selection", "logical")
    formset_class = LogicalFormSet
    formset = formset_class(request.GET)

    if formset.is_valid():
        logger.debug("Formset is valid.")
        data = [f for f in formset.cleaned_data if f]
        
        # Save formset data to session
        request.session['formset_data'] = json.dumps(data)

        results = get_results(data)
        logger.debug(f"Found {len(results)} results.")
    else:
        # If formset is invalid, check if there's saved formset data in session
        formset_data_json = request.session.get('formset_data', None)
        if formset_data_json:
            formset_data = json.loads(formset_data_json)
            results = get_results(formset_data)
            logger.debug("Used formset data from session.")
        else:
            logger.error("Formset is invalid and no session data found.")
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