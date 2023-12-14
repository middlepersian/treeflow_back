import logging
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from treeflow.corpus.models import Section
from .forms import DistanceFormSet, LogicalFormSet, ResultFilterForm
from .models import SearchCriteria, SearchSession
from .logic import get_results

logger = logging.getLogger(__name__)


def change_search_type(request):
    if request.method == "GET" and request.headers.get("hx-request"):
        layout_selection = request.GET.get("layout_selection")

        if layout_selection == "logical":
            formset = LogicalFormSet(queryset=SearchCriteria.objects.none())
        else:
            formset = DistanceFormSet(queryset=SearchCriteria.objects.none())

    return render(
        request,
        "search/formset.html",
        {"formset": formset, "layout_selection": layout_selection},
    )


def results_view(request):
    user = request.user.id
    session_id = request.session.session_key

    if request.method == "POST":
        page_number = 1
        layout_selection = request.POST.get("layout_selection", "distance")
        formset = (
            LogicalFormSet(request.POST)
            if layout_selection == "logical"
            else DistanceFormSet(request.POST)
        )

        if formset.is_valid():
            instances = formset.save(commit=False)
            data = formset.cleaned_data
            logger.debug(f"Submitted data: {data}")

            results = get_results(data)
            logger.debug(f"Results: {results}")

            section_ids = list(results.values_list("id", flat=True))

        try:
            search_session, created = SearchSession.objects.get_or_create(
                user=user,
                session_id=session_id,
                results=section_ids,
            )

            for instance in instances:
                instance.save()
                search_session.formset.add(instance)

            search_session.save()
            logger.debug(f"Search session updated: {search_session}")

        except Exception as e:
            logger.debug(f"Session could not be created: {e}")

    elif request.method == "GET" and "page" in request.GET:
        layout_selection = request.GET.get("layout_selection", "distance")
        page_number = request.GET.get("page", 1)
        results = Section.objects.none()

        try:
            search_session = SearchSession.objects.get(
                user=user, session_id=session_id
            )
            formset_data = search_session.formset.all()
            # TODO: Remove layout/formset from results
            formset = (
                LogicalFormSet(queryset=formset_data)
                if layout_selection == "logical"
                else DistanceFormSet(queryset=formset_data)
            )
            results = Section.objects.filter(id__in=search_session.results)

            logger.debug(f"Search session found: {search_session}")
            logger.debug(f"Loaded the following results: {results}")

        except Exception as e:
            logger.debug(f"Search session could not be found: {e}")

    queries = [form["query"] for form in formset] if formset else []
    paginator = Paginator(results, 10) if results else None
    page_obj = paginator.get_page(page_number) if paginator else None

    return render(
        request,
        "search/results.html",
        {
            "page_obj": page_obj,
            "queries": queries,
        },
    )

def search_page(request):
    formset = DistanceFormSet(queryset=SearchCriteria.objects.none())
    layout_selection = request.GET.get("layout_selection", "distance")

    context = {
        "formset": formset,
        "layout_selection": layout_selection,
    }

    return render(request, "pages/search.html", context)
