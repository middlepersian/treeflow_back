import logging
from django.views.decorators.http import require_GET
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from treeflow.corpus.models import Section, Text
from .forms import DistanceFormSet, LogicalFormSet, ResultFilterForm
from .models import SearchCriteria, SearchSession
from .logic import get_results, narrow_results

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
    text_id = request.GET.get("text", "")
    section_id = request.GET.get("section", "")
    results = Section.objects.none()
    search_session = SearchSession.objects.none()
    text = Text.objects.get(id=text_id) if text_id else Text.objects.none()
    section = Section.objects.get(id=section_id) if section_id else Section.objects.none()
    filter_form = ResultFilterForm(initial={"text": text, "section": section})
    
    if request.method == "POST":
        logger.info("POST request received.")
        layout_selection = request.POST.get("layout_selection", "logical")
        formset = (
            LogicalFormSet(request.POST)
            if layout_selection == "logical"
            else DistanceFormSet(request.POST)
        )

        if formset.is_valid():
            data = [f for f in formset.cleaned_data if f]
            logger.debug(f"Submitted data: {data}")

            try:
                results = get_results(data)
                logger.debug(f"Found {len(results)} results.")
            except Exception as e:
                logger.error(f"Could not retrieve results: {e}")

            queries = [form["query"] for form in data if "query" in form]
            try:
                section_ids = [section.id for section in results]
                logger.debug(f"Found {len(section_ids)} section IDs.")
                results = Section.objects.filter(id__in=section_ids).prefetch_related("sectiontoken_set", "sectiontoken_set__token", "senses")
                # log the length of the results
                logger.debug(f"Found {len(results)} sections with the ids.")          
            except Exception as e:
                logger.error(f"Error while extracting section IDs: {e}")
                section_ids = []
                results = Section.objects.none()

            search_session = get_or_create_session(request, queries, section_ids)


    elif request.method == "GET":
        logger.info("GET request received.")
        page_number = request.GET.get("page", 1)
        queries = request.GET.getlist("query", [])
        filters = {"text": text_id, "section": section_id}

        try:
            search_session = get_or_create_session(request, queries)
            results = Section.objects.filter(id__in=search_session.results)

            if text_id or section_id:
                results = narrow_results(results, text_id, section_id)
                logger.debug(f"Narrowed down to {len(results)} results.")

        except Exception as e:
            logger.debug(f"Search session could not be found: {e}")

    for result in results:
        result.senses_list = list(result.senses.all())
        result.sectiontoken_list = list(result.sectiontoken_set.all())

    paginator = Paginator(results, 10)
    page_obj = paginator.get_page(page_number) if paginator else None
    logger.info(f"Page object: {page_obj}")

    return render(
        request,
        "search/results.html",
        {
            "page_obj": page_obj,
            "queries": queries,
            "text_id": text_id,
            "section_id": section_id,
            "filter_form": filter_form,
        },
    )

@require_GET
def search_page(request):
    queryset = SearchCriteria.objects.none()
    results = Section.objects.none()
    layout_selection = request.GET.get("layout_selection", "logical")
    filter_form = ResultFilterForm()
    formset = (
        LogicalFormSet(queryset=queryset)
        if layout_selection == "logical"
        else DistanceFormSet(queryset=queryset)
    )
    context = {
        "filter_form": filter_form,
        "formset": formset,
        "layout_selection": layout_selection,
        "results": results,
    }

    if request.headers.get("HX-Request"):
        return render(request, "search/_partial.html", context)

    return render(request, "pages/search.html", context)
