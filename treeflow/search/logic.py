from treeflow.corpus.models import Section, SectionToken, Token
from django.db.models import Q,Prefetch,QuerySet,Count




def search(mode="logical",scope="token",*args,**kwargs):
    ...

def logical_search(scope="token",*args,**kwargs):
    if scope == "token":
        ...
    elif scope == "section":
        ...
    return None

def token_search(criterias:list[dict],logical_operator="AND"):
    queries = []
    operators = []
    candidates = SectionToken.objects.all()
    for criteria in criterias:
        scope = criteria.get("scope","token")
        query_field = criteria.get("query_field","transcription")
        query_type = criteria.get("query_type","contains")
        case_insensitive_prefix = criteria.get("case_insensitive_prefix","")
        value = criteria.get("value","")
        logical_operator = criteria.get("logical_operator","AND")
        query_lookup = {
            "exact": f"{scope}__{query_field}__{case_insensitive_prefix}exact",
            "prefix": f"{scope}__{query_field}__{case_insensitive_prefix}startswith",
            "suffix": f"{scope}__{query_field}__{case_insensitive_prefix}endswith",
            "regex": f"{scope}__{query_field}__{case_insensitive_prefix}regex",
            "contains": f"{scope}__{query_field}__{case_insensitive_prefix}contains",
        }
        query = Q(**{query_lookup.get(query_type, query_lookup["contains"]): value})
        queries.append(query)
        operators.append(logical_operator)
    
    for i,query in enumerate(queries):
        if i == 0:
            candidates = candidates.filter(query)
            continue
        logical_operator = operators[i]
        if logical_operator == "AND":
            candidates = candidates.filter(query)
        elif logical_operator == "OR":
            candidates = candidates | candidates.filter(query)
        elif logical_operator == "NOT":
            candidates = candidates.exclude(query)
    candidates = candidates.prefetch_related("section","section__tokens")
    return candidates
    

def distance_search(scope="token",*args,**kwargs):
    if scope == "token":
        ...
    elif scope == "section":
        ...
    return None

