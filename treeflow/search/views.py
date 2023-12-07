from django.shortcuts import render
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
    results = None
    queries = []

    if request.method == "POST":
        if request.POST.get("formset-type") == "logical":
            formset = LogicalFormSet(request.POST)
            layout_selection = "logical"
        elif request.POST.get("formset-type") == "distance":
            formset = DistanceFormSet(request.POST)
            layout_selection = "distance"

        if formset.is_valid():
            formset.save()
            results = get_results(formset.cleaned_data)
            queries = [form.cleaned_data['query'] for form in formset]
            print(results)
        else:
            results = None
            print(formset.errors)

    print(queries)
    context = {
        "formset": formset,
        "layout_selection": layout_selection,
        "results": results,
        "queries": queries,
    }

    return render(request, "pages/search.html", context)
