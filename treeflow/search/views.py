from django.shortcuts import render
from .forms import SearchFormSet
from .models import SearchCriteria
# from .logic import process_search_inputs


def search_page(request):
    results = None
    formset = SearchFormSet(queryset=SearchCriteria.objects.none())

    if request.method == "POST":
        formset = SearchFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.save()
        else:
            print(formset.errors)

    context = {"formset": formset, "results": results}

    return render(request, "pages/search.html", context)
