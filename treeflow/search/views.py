import json
import logging
from typing import Dict, List

from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q, QuerySet
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.http import require_GET

from uuid import uuid4

from treeflow.corpus.models import Section, SectionToken, Token

from django.forms import BaseModelFormSet

from .forms import LogicalFormSet
from .forms import DistanceFormSet
from .models import SearchCriteria

logger = logging.getLogger(__name__)

queries = set()


@require_GET
def search_page(request):
    """
    Render the search page with the appropriate form and layout selection.
    """
    layout_selection = request.GET.get("layout_selection", "logical-section")
    queryset = SearchCriteria.objects.none()
    formset_class = LogicalFormSet
    if "distance" in layout_selection:
        formset_class = DistanceFormSet
    formset = formset_class(queryset=queryset)
    
    queries.clear()

    context = {
        # "filter_form": filter_form,
        "formset": formset,
        "layout_selection": layout_selection,
        "results": Section.objects.none(),
    }

    # Clear session data
    if 'results' in request.session:
        del request.session['results']
    if 'formset_data' in request.session:
        del request.session['formset_data']

    if request.headers.get("HX-Request"):
        return render(request, "search/_partial.html", context)

    return render(request, "pages/search.html", context)

def results_view(request):
    """
    Handle search results display based on GET or POST requests.
    """
    page_number = request.GET.get("page", 1)
    results_per_page = request.GET.get("results_per_page", 10)
    results = None
    key = None 
    queries.clear()

    
    if (not request.GET.get("just_pages", False)):
        try:
            layout_selection = request.GET.get("layout_selection", "logical-section")
            logger.debug(f"Layout selection: {layout_selection}")
            if "logical" in layout_selection:
                formset = LogicalFormSet(request.GET)
            else:
                formset = DistanceFormSet(request.GET)
            
            query_formset_type = layout_selection

            results, key = handle_request(request,formset,query_formset_type)
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            results = Section.objects.none()
    else:
        logger.debug("Used results data from session.")
        results_json = request.session.get('results', '[]')
        results = json.loads(results_json)

        formset_data_json = request.session.get('formset_data', None)
        json.loads(formset_data_json)
        formset_data = json.loads(formset_data_json)
        key = request.session.get("key", None)
        for form in formset_data:
            queries.add(form["query"])

    # Ensure results is a queryset before prefetching
    if not isinstance(results, QuerySet):
        if type(results) == list:
            results = Section.objects.filter(id__in=[r['id'] for r in results])
        else:
            results = Section.objects.filter(id__in=[r.id for r in results])

    results_all = False
    if results_per_page == "All":
        results_all = True
        results_per_page = results.count()

    results.prefetch_related("section__tokens", "section__tokens__lemmas", "section__tokens__pos_token","section__tokens__senses")
    paginator = Paginator(results, results_per_page)
    page_obj = paginator.get_page(page_number)

    total_pages = paginator.num_pages

    return render(
        request,
        "search/results.html",
        {
            "page_obj": page_obj,
            "queries": queries,
            "key": key,
            "total_pages": total_pages,
            "results_settings": {
                "per_page": results_per_page,
                "steps": [10, 20, 30, 100, 200],
                "is_all": results_all,
            }
        },
    )

def handle_request(request: HttpRequest,formset:BaseModelFormSet,query_formset_type) -> QuerySet:
    """
    Handle form submission for search results.
    """
    key = None
    if formset.is_valid():
        logger.debug("Formset is valid.")
        data = [f for f in formset.cleaned_data if f]
        # Save formset data to session
        request.session['formset_data'] = json.dumps(data)
        
        logger.debug(f"Before get_results")
        results,key= get_results(data,query_formset_type)
        logger.debug(f"After get_results")
        logger.debug(f"Found {len(results)} results.")
        request.session['results'] = json.dumps(list(results.values()), cls=DjangoJSONEncoder)
        request.session["key"] = key
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
    
    return results, key

def get_results(criteria: List,query_formset_type) -> QuerySet:
    """
    Retrieve search results based on given criteria.
    """
    
    key = None
    if not criteria:
        logger.error("No criteria provided")
        return Section.objects.none()

    queries.clear()

    for form in criteria:
        queries.add(form["query"])

    anchor_criterion = criteria[0]
    filters = criteria[1:]
   
    if query_formset_type == "logical-section":
        logger.debug("Retrieving tokens based on anchor criterion.")
        anchor_tokens, key = retrieve_tokens(anchor_criterion)
        sections = identify_sections(anchor_tokens)
        if filters:
            if "logical_operator" in anchor_criterion:
                sections = filter_sections_by_logic(sections, filters, key)
    
    elif query_formset_type == "logical-token":
        anchor_tokens, key = retrieve_tokens_with_filters(criteria)
        sections = identify_sections(anchor_tokens)

    elif query_formset_type == "distance-section":
        sections, key = distance_search(criteria)
    else:
        return Section.objects.none()
    
    return sections, key

def retrieve_tokens(criteria: Dict, key=None) -> QuerySet:
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
        "exact": f"token__{query_field}__{case_insensitive_prefix}{query_type}",
        "prefix": f"token__{query_field}__{case_insensitive_prefix}{query_type}",
        "suffix": f"token__{query_field}__{case_insensitive_prefix}{query_type}",
        "regex": f"token__{query_field}__{case_insensitive_prefix}{query_type}",
        "contains": f"token__{query_field}__{case_insensitive_prefix}{query_type}",
    }
    logger.debug(f"Query lookup: {query_lookup.get(query_type, query_lookup['contains'])} : {value}")
    query = Q(**{query_lookup.get(query_type, query_lookup["contains"]): value})

    for k, v in criteria.items():
        if v and not any(x in k for x in ["logical", "distance", "id"]):
            query &= Q(**{k: v})

    candidates = SectionToken.objects.filter(query).prefetch_related("token", "section")
    logger.debug(f"Found {candidates.count()} candidates.")
    logger.debug(f"Query: {candidates.query}")
    
    if not key:
        key = f"{uuid4()}"
        if candidates:
            candiates_list = list(candidates.values_list("token_id",flat=True))
            logger.debug(f"ANCHORS: Setting cache with key: {key} and {len(candiates_list)} tokens.")
            cache.set(key+"anchors",candiates_list, timeout=120)
    else:
        
        if candidates:
            candiates_list = list(candidates.values_list("token_id",flat=True))
            logger.debug(f"HITS: Setting cache with key: {key} and {len(candiates_list)} tokens.")
            cache.set(key+"hits",candiates_list, timeout=120)
    
    return candidates, key

def retrieve_tokens_with_filters(filters: List[Dict]) -> QuerySet:
    query = Q(section__type__exact="sentence")
    sectionTokens = SectionToken.objects.filter(query)

    logger.debug("213 filtering tokens with filters")
    logger.debug(f"214 Filters: {filters}")
    for i,filter in enumerate(filters):
        criteria = filter.copy()
        value = criteria.pop("query", None)
        query_field = criteria.pop("query_field", "")
        query_type = criteria.pop("query_type", "contains")
        case_sensitive = criteria.pop("case_sensitive", False)
        case_insensitive_prefix = "" if case_sensitive else "i"
        
        query_lookup = {
        "exact": f"token__{query_field}__{case_insensitive_prefix}{query_type}",
        "startswith": f"token__{query_field}__{case_insensitive_prefix}{query_type}",
        "endwith": f"token__{query_field}__{case_insensitive_prefix}{query_type}",
        "regex": f"token__{query_field}__{case_insensitive_prefix}{query_type}",
        "contains": f"token__{query_field}__{case_insensitive_prefix}{query_type}",
        }

        if i == 0 or criteria['logical_operator'] == "AND":
            query &= Q(**{query_lookup.get(query_type, query_lookup["contains"]): value})
        elif criteria['logical_operator'] == "OR":
            query |= Q(**{query_lookup.get(query_type, query_lookup["contains"]): value})
        elif criteria['logical_operator'] == "NOT":
            query &= ~Q(**{query_lookup.get(query_type, query_lookup["contains"]): value})

        for k, v in criteria.items():
            if v and not any(x in k for x in ["logical", "distance", "id"]):
                query &= Q(**{k: v})
        

    candidates = SectionToken.objects.filter(query).prefetch_related("token", "section")
    key = f"{uuid4()}"
    if candidates:
        cache.set(key+"anchors", list(Token.objects.filter(id__in=[c.token.id for c in candidates]).only("id").values_list("id",flat=True)), timeout=120)

    return candidates, key

        
def identify_sections(tokens: QuerySet) -> QuerySet:
    """
    Identify sections related to a list of SectionTokens.
    """
    
    logger.debug(f"Tokens: {tokens}")
    token_ids = tokens.values_list('id', flat=True)
    return Section.objects.filter(sectiontoken__id__in=token_ids,type="sentence").distinct()

def filter_sections_by_logic(candidate_sections: QuerySet, token_search_inputs: List[Dict], key) -> QuerySet:
    """
    Filter sections based on logical operators (AND/OR).
    """
    for token_search_input in token_search_inputs:
        filter_tokens, key = retrieve_tokens(token_search_input,key)
        filter_sections = identify_sections(filter_tokens)
        
        if token_search_input.get("logical_operator") == "AND":
            candidate_sections = candidate_sections.filter(id__in=filter_sections.values_list("id", flat=True))
        else:  # OR
            candidate_sections |= filter_sections
            
    # update cache with hits
    

    return candidate_sections

def distance_search(filter_tokens: List[Dict]) -> QuerySet:
    anchor_criteria = filter_tokens[0]
    search_filters = filter_tokens[1:]
    sections = distance(anchor_criteria,search_filters)
    return sections

def create_query_dict_from_criteria(criteria: Dict,model_ref="",) -> dict:
    _criteria = criteria.copy()
    value = _criteria.pop("query", None)
    query_field = _criteria.pop("query_field", "")
    query_type = _criteria.pop("query_type", "contains")
    case_sensitive = _criteria.pop("case_sensitive", False)
    case_insensitive_prefix = "" if case_sensitive else "i"
    model_ref = model_ref + "__" if model_ref else ""

    return {f"{model_ref}{query_field}__{case_insensitive_prefix}{query_type}": value}

def distance(anchor_criteria: dict, search_criteria: list[dict]):
    key = None
    section_ids = []
    anchor_token_ids = []
    search_token_ids = []
    
    sections = Section.objects.none()
    
    # First: Get all Sections that contain the anchor Tokens
    anchors = Section.objects.filter(
        Q(**create_query_dict_from_criteria(anchor_criteria, "tokens")),
        tokens__number_in_sentence__isnull=False,
        type="sentence"
    ).distinct()

    # Filtering for sections that additionaly have all search criteria
    for criteria in search_criteria:
        anchors = anchors.filter(
            Q(**create_query_dict_from_criteria(criteria, "tokens")),
        )
    logger.debug(f"Found {anchors.count()} anchors.")
    
    # Second: Check for each anchor if there is one anchor token, that meets all search criteria
    for anchor in anchors:
        # Get the tokens of the anchor, that meet the anchor criteria
        anchor_tokens = anchor.tokens.filter(Q(**create_query_dict_from_criteria(anchor_criteria)))
        anchor_tokens_temp = anchor_tokens

        anchor_token_ids.append(anchor_tokens.values_list('id', flat=True))
        
        # get the number of the anchor tokens in the sentence
        anchor_tokens = anchor_tokens.values_list('number_in_sentence', flat=True)
        
        hit_candidates = {
            anchor_token: [] for anchor_token in anchor_tokens
        }
        
        search_token_canditates = []
        criteria_resutlts = []
        
        """
        Now get the distance and distance type for each search criteria
        """
        for i,criteria in enumerate(search_criteria):
            distance = criteria.get("distance", 1)
            distance_type = criteria.get("distance_type", "after")
            
            
            # possible numbers for the search tokens depending on the distance and distance type
            numbers = [a + distance for a in anchor_tokens] + [a - distance for a in anchor_tokens]
            if distance_type == "after":
                numbers = [a + distance for a in anchor_tokens]
            elif distance_type == "before":
                numbers = [a - distance for a in anchor_tokens]

            query = {"number_in_sentence__in": numbers}
            # check if there is at least one token that meets the search criteria
            # if so, add the token to the search_token_ids and append True to the criteria_results
            # to check if all criteria are met
            if anchor.tokens.filter(Q(Q(**create_query_dict_from_criteria(criteria), **query))).exists():
                criteria_resutlts.append(True)
                search_token_ids.append(anchor.tokens.filter(Q(Q(**create_query_dict_from_criteria(criteria), **query))).values_list('id', flat=True))
                continue
            
            # if there is no token that meets the search criteria, add False to the criteria_results
            criteria_resutlts.append(False)
            
        # if there are more than one anchor token, that meets the anchor criteria, check if there is at least one token that meets all search criteria
        if len(anchor_tokens_temp) > 1:
            for anchor_token in anchor_tokens_temp:
                query_list = []
                for criteria in search_criteria:
                    distance = criteria.get("distance", 1)
                    distance_type = criteria.get("distance_type", "after")
                    numbers = [anchor_token.number_in_sentence + distance, anchor_token.number_in_sentence - distance]
                    if distance_type == "after":
                        numbers = [anchor_token.number_in_sentence + distance]
                    elif distance_type == "before":
                        numbers = [anchor_token.number_in_sentence - distance]
                    query = {"number_in_sentence__in": numbers}
                    query_list.append(Q(Q(**create_query_dict_from_criteria(criteria), **query)))
                anchor_tokens_temp1 = anchor_tokens_temp.exclude(id=anchor_token.id)
                
                
                for query in query_list:
                    anchor_tokens_temp1 = anchor_tokens_temp1.filter(query)
                
                
                if anchor_tokens_temp1.exists():
                    criteria_resutlts.append(True)
                    search_token_ids.append(anchor_tokens_temp1.values_list('id', flat=True))
                    break
                else:
                    criteria_resutlts.append(False)
                    
        if all(criteria_resutlts):
            section_ids.append(anchor.id)
    sections = Section.objects.filter(id__in=section_ids).distinct().prefetch_related("tokens","text")
    
    
    key = f"{uuid4()}"
    if section_ids:
        cache.set(key+"hits", list(Token.objects.filter(id__in=[t for tokens in search_token_ids for t in tokens]).only("id").values_list("id",flat=True)), timeout=120)
        cache.set(key+"anchors", list(Token.objects.filter(id__in=[t for tokens in anchor_token_ids for t in tokens]).only("id").values_list("id",flat=True)), timeout=120)

    return sections, key

    
def get_anchors_from_cache(request,key_value) -> list:
    """Get anchors from cache.

    Args:
        request (HttpRequest): The HTTP request object.
        key_value (str): The key value used to retrieve anchors from cache.

    Returns:
        list: A list of anchors and hits.
    """
    anchors = cache.get(str(key_value)+"anchors",[])
    hits = cache.get(str(key_value)+"hits",[])
    
    # Update Cache
    cache.set(str(key_value)+"anchors",anchors, timeout=120)
    cache.set(str(key_value)+"hits",hits, timeout=120)
    return JsonResponse({"anchors":anchors,"hits":hits})