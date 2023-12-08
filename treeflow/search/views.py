from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from treeflow.corpus.models import Section
from .forms import DistanceFormSet, LogicalFormSet, ResultFilterForm
from .models import SearchCriteria
from .logic import get_results


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


def search_page(request):
    formset = DistanceFormSet(queryset=SearchCriteria.objects.none())
    layout_selection = "distance"
    results = []
    queries = []
    page_number = request.GET.get("page")

    if request.method == "POST":
        layout_selection = request.POST.get("formset-type")

        if layout_selection == "logical":
            formset = LogicalFormSet(request.POST)
        elif layout_selection == "distance":
            formset = DistanceFormSet(request.POST)

        if formset.is_valid():
            formset.save()
            results = get_results(formset.cleaned_data)
            queries = [form.cleaned_data["query"] for form in formset]
            
            request.session["form_data"] = request.POST
            request.session["queries"] = queries
            request.session["results"] = [str(result.id) for result in results]
            return redirect('search:search_page')
        else:
            results = Section.objects.none()

    else:
        if "results" in request.session:
            results = Section.objects.filter(id__in=request.session["results"])
        if "queries" in request.session:
            queries = request.session["queries"]
        if "form_data" in request.session:
            data = request.session["form_data"]
            layout_selection = data.get("formset-type")
            if layout_selection == "logical":
                formset = LogicalFormSet(data)
            elif layout_selection == "distance":
                formset = DistanceFormSet(data)

    paginator = Paginator(results, 10) if results else None
    page_obj = paginator.get_page(page_number) if paginator else None

    context = {
        "formset": formset,
        "layout_selection": layout_selection,
        "page_obj": page_obj,
        "queries": queries,
    }

    return render(request, "pages/search.html", context)
