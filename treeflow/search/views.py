import json
import logging
import time
from typing import Dict, List

from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q, QuerySet, Subquery, OuterRef, F
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.postgres.aggregates import StringAgg
import re


from treeflow.corpus.models import Section, SectionToken, Token

from django.db import connection

from django.forms import BaseModelFormSet

from .forms import LogicalFormSet
from .forms import DistanceFormSet
from .models import SearchCriteria
from django.db.models import Q, Subquery, OuterRef, F, Value

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

            results = handle_request(request,formset,query_formset_type)
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
    if formset.is_valid():
        logger.debug("Formset is valid.")
        data = [f for f in formset.cleaned_data if f]
        # Save formset data to session
        request.session['formset_data'] = json.dumps(data)
        
        logger.debug(f"Before get_results")
        results= get_results(data,query_formset_type)
        logger.debug(f"After get_results")
        logger.debug(f"Found {len(results)} results.")
        request.session['results'] = json.dumps(list(results.values()), cls=DjangoJSONEncoder)
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

def get_results(criteria: List,query_formset_type) -> QuerySet:
    """
    Retrieve search results based on given criteria.
    """
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
        anchor_tokens = retrieve_tokens(anchor_criterion)
        sections = identify_sections(anchor_tokens)
        if filters:
            if "logical_operator" in anchor_criterion:
                sections = filter_sections_by_logic(sections, filters)
    
    elif query_formset_type == "logical-token":
        anchor_tokens = retrieve_tokens_with_filters(criteria)
        sections = identify_sections(anchor_tokens)

    elif query_formset_type == "distance-section":
        sections = distance(criteria)
    else:
        return Section.objects.none()
    
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
    logger.debug(f"Query lookup: {query_lookup.get(query_type, query_lookup['contains'])} : {value}")
    query = Q(**{query_lookup.get(query_type, query_lookup["contains"]): value})

    for k, v in criteria.items():
        if v and not any(x in k for x in ["logical", "distance", "id"]):
            query &= Q(**{k: v})

    candidates = SectionToken.objects.filter(query).prefetch_related("token", "section")
    logger.debug(f"Found {candidates.count()} candidates.")
    logger.debug(f"Query: {candidates.query}")
    return candidates

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
        "exact": f"token__{query_field}__{case_insensitive_prefix}exact",
        "prefix": f"token__{query_field}__{case_insensitive_prefix}startswith",
        "suffix": f"token__{query_field}__{case_insensitive_prefix}endswith",
        "regex": f"token__{query_field}__{case_insensitive_prefix}regex",
        "contains": f"token__{query_field}__{case_insensitive_prefix}contains",
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
        
        logger.debug(f"Query lookup: query: {query} : {value}")

    logger.debug(f"Query lookup: {query} : {value}")
    candidates = SectionToken.objects.filter(query).prefetch_related("token", "section")
    logger.debug(f"Found {candidates.count()} candidates.")
    logger.debug(f"Query: {candidates.query}")
    return candidates

        
def identify_sections(tokens: QuerySet) -> QuerySet:
    """
    Identify sections related to a list of SectionTokens.
    """
    token_ids = tokens.values_list('id', flat=True)
    return Section.objects.filter(sectiontoken__id__in=token_ids,type="sentence").distinct()

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

def distance(filter_tokens: List[Dict]) -> QuerySet:
    anchor_criteria = filter_tokens[0]
    search_filters = filter_tokens[1:]
    sections = distance5(anchor_criteria,search_filters)
    #sections = find_sentences_with_all_criteria(anchor_criteria, search_filters)
    #sections = sectiontokens_by_distance_2(anchor_criteria,search_filters)
    return sections

def create_query_dict_from_criteria(criteria: Dict,model_ref="",) -> dict:
    _criteria = criteria.copy()
    value = _criteria.pop("query", None)
    query_field = _criteria.pop("query_field", "")
    query_type = _criteria.pop("query_type", "contains")
    case_sensitive = _criteria.pop("case_sensitive", False)
    case_insensitive_prefix = "" if case_sensitive else "i"
    model_ref = model_ref + "__" if model_ref else ""
    query_type_str = ""
    match query_type:
        case "exact":
            query_type_str = "exact"
        case "prefix":
            query_type_str = "startswith"
        case "suffix":
            query_type_str = "endswith"
        case "regex":
            query_type_str = "regex"
        case "contains":
            query_type_str = "contains"
        case _:
            query_type_str = "contains"

    return {f"{model_ref}{query_field}__{case_insensitive_prefix}{query_type_str}": value}

def find_sentences_with_all_criteria(anchor_attrs:dict, search_filters:list[dict]):
    
    query = Q(**create_query_dict_from_criteria(anchor_attrs,"tokens"))
    queries = []
    for filter in search_filters:
        queries.append(Q(**create_query_dict_from_criteria(filter,"tokens")))

    sections = Section.objects.filter(query, type="sentence").distinct()
    for _query in queries:
        sections = sections.filter(_query)
    

    for section in sections:
        anchor_token = section.tokens.filter(**create_query_dict_from_criteria(anchor_attrs), number_in_sentence__isnull=False).values_list('number_in_sentence', flat=True)
        if not anchor_token:
            sections = sections.exclude(id=section.id)
            continue
        for criteria in search_filters:
            _criteria = criteria.copy()
            distance = _criteria.pop("distance", 1)
            search_token = section.tokens.filter(**create_query_dict_from_criteria(_criteria), number_in_sentence__isnull=False,
                                                 ).values_list('number_in_sentence', flat=True)
            if not search_token:
                sections = sections.exclude(id=section.id)
                continue
            if search_token and anchor_token:
                match _criteria.get("distance_type","after"):
                    case "after":
                        if search_token[0] == anchor_token[0] + distance:
                            continue
                        else:
                            sections = sections.exclude(id=section.id)
                    case "before":
                        if search_token[0] == anchor_token[0] - distance:
                            continue
                        else:
                            sections = sections.exclude(id=section.id)
                    case _:
                        if search_token[0] == anchor_token[0] + distance:
                            continue
                        elif search_token[0] == anchor_token[0] - distance:
                            continue
                        else:
                            sections = sections.exclude(id=section.id)
                
            #         continue
            #     if search_token[1] == anchor_token[1] + distance:
            #         continue
            #     if search_token[1] == anchor_token[1] - distance:
            #         continue
            #     sections = sections.exclude(id=section.id) 
        
    logger.debug(f"Found {sections.count()} sections.")
    return sections

def sectiontokens_by_distance(anchor_criteria:dict,search_criteria:list[dict]):
    anchor_query = Q(**create_query_dict_from_criteria(anchor_criteria,"token"))
    anchors = SectionToken.objects.filter(anchor_query,section__type="sentence",token__number_in_sentence__isnull=False).prefetch_related("section","token")
  
    search_tokens = SectionToken.objects.none()
    sectionIds = []
    for anchor in anchors:
        for filter in search_criteria:
            distance = filter.get("distance",1)
            distance_type = filter.get("distance_type","after")
            if distance_type == "after":
                search_tokens |= SectionToken.objects.filter(
                    Q(**create_query_dict_from_criteria(filter, "token")),
                    section__type="sentence",
                    token__number_in_sentence__isnull=False,
                    token__number_in_sentence=F(anchor.token.number_in_sentence + distance)
                ).prefetch_related("section", "token")
            elif distance_type == "before":
                search_tokens |= SectionToken.objects.filter(
                    Q(**create_query_dict_from_criteria(filter, "token")),
                    section__type="sentence",
                    token__number_in_sentence__isnull=False,
                    token__number_in_sentence=F(anchor.token.number_in_sentence - distance)
                ).prefetch_related("section", "token")
            else:
                search_tokens |= SectionToken.objects.filter(
                    Q(**create_query_dict_from_criteria(filter, "token")),
                    Q(token__number_in_sentence__in=[F(anchor.token.number_in_sentence + distance),F(anchor.token.number_in_sentence - distance)]
                    ),
                    token__number_in_sentence__isnull=False,
                    section__type="sentence"
                ).prefetch_related("section", "token")

    sectionIds = search_tokens.values_list('section__id', flat=True)
    anchor_sectionIds = anchors.values_list('section__id', flat=True)
    sectionIds = list(set(sectionIds) & set(anchor_sectionIds))
    sections = Section.objects.filter(id__in=sectionIds).distinct()

    return sections

def annotate_sections_by_search_criteria(sections: QuerySet, search_criteria: List[Dict]) -> QuerySet:
    """
    Annotate sections with search criteria.
    """
    for criteria in search_criteria:
        sections = sections.annotate(
            **{f"{criteria['query_field']}_{criteria['query_type']}": F("tokens__" + criteria['query_field'])}
        )

    return sections

def sectiontokens_by_distance_2(anchor_criteria: dict, search_criteria: list[dict]):
    anchor_query = Q(**create_query_dict_from_criteria(anchor_criteria, "token"))
    anchors = SectionToken.objects.filter(anchor_query, section__type="sentence",token__number_in_sentence__isnull=False).distinct().prefetch_related("token")
    search = SectionToken.objects.none()
    sections = Section.objects.none()

    if not anchors.exists():
        return sections
    
    for filter in search_criteria:
        hit = SectionToken.objects.filter(
            Q(**create_query_dict_from_criteria(filter, "token")),
            section__type="sentence",
            token__number_in_sentence__isnull=False
        ).prefetch_related("token").annotate(
            distance=Value(filter.get("distance", 1)), 
        ).annotate(
            distance_type=Value(filter.get("distance_type", "after")),
        )
        search |= hit 

    logger.debug(f"Found {anchors.count()} anchors.")
    anchor_ids = anchors.values_list('section_id', flat=True).distinct()
    search_ids = search.values_list('section_id', flat=True).distinct()

    anchor_tokens = anchors.values_list('section_id','token_id','token__number_in_sentence')
    search_tokens = search.values_list('section_id','token_id','token__number_in_sentence','distance','distance_type')



    # find SectionTokens that are in anchor_sections and search_sections

    section_ids = list(set(anchor_ids) & set(search_ids))
    
    for id in section_ids:
        for anchor in anchor_tokens.filter(section_id=id):
            anchor_number = anchor[2]
            for search in search_tokens.filter(section_id=id):
                search_number = search[2]
                search_distance = search[3]
                search_distance_type = search[4]
                if search_number == anchor_number + search_distance and search_distance_type == "after":
                    sections |= Section.objects.filter(id=id)
                elif search_number == anchor_number - search_distance and search_distance_type == "before":
                    sections |= Section.objects.filter(id=id)
                elif search_number in [anchor_number + search_distance,anchor_number - search_distance] and search_distance_type == "both":
                    sections |= Section.objects.filter(id=id)
    sections = sections.distinct().prefetch_related("tokens")
    logger.debug(f"Found {sections.count()} sections.")
    
    # sections = Section.objects.filter(id__in=section_ids).distinct().order_by('id').prefetch_related("tokens","tokens__senses","tokens__lemmas","tokens__pos_token")

    # search_sections = SectionToken.objects.filter(Q(section_id__in=sections.values_list('id', flat=True)),~Q(token_id__in=anchor_tokens))

    return sections
    
def get_range_numbers_for_distance_to(anchor_token:Token,search_criteria:list[dict]) -> tuple[int,int]:
    number = anchor_token.number_in_sentence
    max_l_distance = 0
    max_r_distance = 0
    for criteria in search_criteria:
        distance = criteria.get("distance",1)
        distance_type = criteria.get("distance_type","after")
        match distance_type:
            case "after":
                max_r_distance = distance if distance > max_r_distance else max_r_distance
            case "before":
                max_l_distance = distance if distance > max_l_distance else max_l_distance
            case _:
                if distance > max_r_distance:
                    max_r_distance = distance
                if distance > max_l_distance:
                    max_l_distance = distance
        if distance > max_distance:
            max_distance = distance

    return (
        number - max_l_distance,
        number + max_r_distance)

def get_tokens_in_range(section,anchor_token,search_criteria:list[dict]):
    range = get_range_numbers_for_distance_to(anchor_token,search_criteria)
    if anchor_token.section.tokens.count() < range[1]:
        return SectionToken.objects.none()
    if range[0] < 0:
        return SectionToken.objects.none()
    
    return section.tokens.filter(number_in_sentence__range=range)

def check_tokens_in_range_for_search_criteria(tokens:QuerySet,search_criteria:list[dict]) -> bool:
    sections = Section.objects.filter(id__in=sections).prefetch_related("tokens")
    for section in sections:
        section.tokens.filter(number_in_sentence__range=range).filter(**create_query_dict_from_criteria(search_criteria[0]))

def distance2(anchor_citeria:dict,search_criteria:List[dict]):
    anchor_sections = SectionToken.objects.filter(**create_query_dict_from_criteria(anchor_citeria,"token"),section__type="sentence").prefetch_related("section","token").annotate(
        distance=F("section__tokens__number_in_sentence") - F("token__number_in_sentence")
    )
    search_sections = SectionToken.objects.none()

    for anchor_section in anchor_sections:
        anchor_number = anchor_section.token.number_in_sentence
        if anchor_number is None:
            continue

        for criteria in search_criteria:
            distance_type = criteria.get("distance_type","both")
            distance = criteria.get("distance",1)
            
            match distance_type:
                case "after":
                    search_dist = [distance]
                case "before":
                    search_dist = [-distance]
                case _:
                    search_dist = [-distance,distance]

            
            hit = anchor_section.section.tokens.filter(
                **create_query_dict_from_criteria(criteria,"token"),
                token__number_in_sentence__isnull=False,
                distance__in=search_dist
            )
            if hit:
                search_sections |= anchor_section

    search_sections = search_sections.values_list('section__id', flat=True).distinct()
    sections = Section.objects.filter(id__in=search_sections).distinct().prefetch_related("tokens")

    return sections
    
def distance3(anchor_criteria:dict,search_criteria:list[dict]):
    anchor_sections = SectionToken.objects.filter(
        Q(**create_query_dict_from_criteria(anchor_criteria,"token")),
        section__type="sentence"
    )
    anchor_section_ids = anchor_sections.values_list('section_id', flat=True)
    anchor_tokens = anchor_sections.values_list('token__id', flat=True)
    section_tokens = SectionToken.objects.none()
    for criteria in search_criteria:
        section_tokens |= SectionToken.objects.filter(
            Q(**create_query_dict_from_criteria(criteria,"token")),
            section__type="sentence",
            section_id__in=anchor_section_ids,
        )

    section_tokens = section_tokens.prefetch_related("section","token")
    section_ids = section_tokens.values_list('section_id', flat=True).distinct()

    sections = Section.objects.filter(id__in=section_ids).distinct().prefetch_related("tokens")
    
    for section in sections:
        section_anchors = section.tokens.filter(Q(**create_query_dict_from_criteria(anchor_criteria)))
        section_search_hits = False
        for anchor_token in section_anchors:
            for criteria in search_criteria:
                distance = criteria.get("distance",1)
                distance_type = criteria.get("distance_type","after")
                query = ""
                if distance_type == "after":
                    query = {"number_in_sentence": anchor_token.number_in_sentence + distance}
                elif distance_type == "before":
                    query = {"number_in_sentence": anchor_token.number_in_sentence - distance}
                else:
                    query = {"number_in_sentence__in": [anchor_token.number_in_sentence + distance,anchor_token.number_in_sentence - distance]}

                section_search_hits = section.tokens.exists(Q(Q(**create_query_dict_from_criteria(criteria),**query)))
        if not section_search_hits:
            sections = sections.exclude(id=section.id)
    
    return sections

def distance4(anchor_criteria:dict,search_criteria:list[dict]):
    anchors = SectionToken.objects.filter(
        Q(**create_query_dict_from_criteria(anchor_criteria,"token")),
        token__number_in_sentence__isnull=False,
        section__type="sentence"
    ).prefetch_related("section","token")
    range = max([x.get("distance",1) for x in search_criteria])

    for anchor in anchors:
        token_sub_section = Token.objects.filter(
            sectiontoken__id=anchor.section_id,
            number_in_sentence__isnull=False,
            number_in_sentence__range=(anchor.token.number_in_sentence - range,anchor.token.number_in_sentence + range)
        )
        for criteria in search_criteria:
            distance = criteria.get("distance",1)
            distance_type = criteria.get("distance_type","after")
            query = ""
            if distance_type == "after":
                query = {"number_in_sentence": anchor.token.number_in_sentence + distance}
            elif distance_type == "before":
                query = {"number_in_sentence": anchor.token.number_in_sentence - distance}
            else:
                query = {"number_in_sentence__in": [anchor.token.number_in_sentence + distance,anchor.token.number_in_sentence - distance]}
            token_sub_section = token_sub_section.filter(Q(Q(**create_query_dict_from_criteria(criteria),**query)))

        if not token_sub_section.exists():
            anchors = anchors.exclude(id=anchor.id)

    section_ids = anchors.values_list('section_id', flat=True).distinct()
    sections = Section.objects.filter(id__in=section_ids).distinct().prefetch_related("tokens")
    return sections


def distance5(anchor_criteria:dict,search_criteria:list[dict]):
    anchors = SectionToken.objects.filter(
        Q(**create_query_dict_from_criteria(anchor_criteria,"token")),
        token__number_in_sentence__isnull=False,
        section__type="sentence"
    ).prefetch_related("section","token")
    anchor_numbers = anchors.values_list('token__number_in_sentence', flat=True)
    search_hits = SectionToken.objects.none()
    for search in search_criteria:
        distance = search.get("distance",1)
        distance_type = search.get("distance_type","after")
        
        search_hits |= anchors.filter(Q(**create_query_dict_from_criteria(search,"section__tokens")))
    
    section_ids = search_hits.values_list('section_id', flat=True).distinct()
    sections = Section.objects.filter(id__in=section_ids).distinct().prefetch_related("tokens")
    return sections
    