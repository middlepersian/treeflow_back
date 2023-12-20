import logging
from django.views.decorators.http import require_GET
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from treeflow.corpus.models import Section
from .forms import DistanceFormSet, LogicalFormSet, ResultFilterForm
from .models import SearchCriteria, SearchSession
from .logic import get_results

logger = logging.getLogger(__name__)


def get_or_create_session(request, queries=None, results=None):
    user = request.user if request.user.is_authenticated else None
    session_id = request.session.session_key

    if request.method == "POST":
        search_session, created = SearchSession.objects.get_or_create(
            user=user,
            session_id=session_id,
            queries=queries,
            defaults={"results": results},
        )

        if created:
            logger.debug(f"Created new search session: {search_session.id}")
        else:
            logger.debug(f"Updated existing search session: {search_session.id}")

    else:
        search_session = SearchSession.objects.filter(
            user=user, session_id=session_id, queries=queries
        ).first()

    return search_session


def results_view(request):
    page_number = 1
    queries = []
    results = Section.objects.none()
    search_session = SearchSession.objects.none()

    if request.method == "POST":
        layout_selection = request.POST.get("layout_selection", "logical")
        formset = (
            LogicalFormSet(request.POST)
            if layout_selection == "logical"
            else DistanceFormSet(request.POST)
        )

        if formset.is_valid():
            data = formset.cleaned_data
            logger.debug(f"Submitted data: {data}")

            try:
                results = get_results(data)
                logger.debug(f"Found {len(results)} results.")
            except Exception as e:
                logger.debug(f"Could not retrieve results: {e}")

            queries = [form["query"] for form in data]
            section_ids = list(results.values_list("id", flat=True).distinct())

            search_session = get_or_create_session(request, queries, section_ids)

    elif request.method == "GET" and "page" in request.GET:
        page_number = request.GET.get("page", 1)
        queries = request.GET.getlist("query", [])

        try:
            search_session = get_or_create_session(request, queries)
            results = Section.objects.filter(id__in=search_session.results)

            logger.debug(f"Search session found: {search_session.id}")

        except Exception as e:
            logger.debug(f"Search session could not be found: {e}")

    paginator = Paginator(
        results.prefetch_related("sectiontoken_set", "sectiontoken_set__token"), 10
    )
    page_obj = paginator.get_page(page_number) if paginator else None

    return render(
        request,
        "search/results.html",
        {
            "page_obj": page_obj,
            "queries": queries,
        },
    )


@require_GET
def search_page(request):
    queryset = SearchCriteria.objects.none()
    results = Section.objects.none()
    layout_selection = request.GET.get("layout_selection", "logical")
    formset = (
        LogicalFormSet(queryset=queryset)
        if layout_selection == "logical"
        else DistanceFormSet(queryset=queryset)
    )
    context = {
        "formset": formset,
        "layout_selection": layout_selection,
        "results": results,
    }

    if request.headers.get("HX-Request"):
        return render(request, "search/_partial.html", context)

    return render(request, "pages/search.html", context)
