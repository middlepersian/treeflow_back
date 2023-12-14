import logging
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from treeflow.corpus.models import Section
from .forms import DistanceFormSet, LogicalFormSet, ResultFilterForm
from .models import SearchCriteria
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
    if request.method == "POST":
        page_number = 1
        layout_selection = request.POST.get("layout_selection", "distance")
        formset = (
            LogicalFormSet(request.POST)
            if layout_selection == "logical"
            else DistanceFormSet(request.POST)
        )

        if formset.is_valid():
            data = formset.cleaned_data
            logger.debug(f"Submitted data: {data}")

            results = get_results(data)
            logger.debug(f"Results: {results}")

            queries = [form.cleaned_data["query"] for form in formset]
            section_ids = list(results.values_list("id", flat=True))

            # TODO Save session data

    elif request.method == "GET":
        # TODO Load session data

        page_number = request.GET.get("page", 1)
        results = Section.objects.none()

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
