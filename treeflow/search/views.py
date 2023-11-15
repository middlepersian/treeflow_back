from django.shortcuts import render, redirect
from .forms import SearchFormSet


def search_page(request):
    formset = SearchFormSet(request.POST or None)

    if request.method == "POST" and formset.is_valid():
        for form in formset:
            form.save()

    return render(request, "search/search_page.html", {"formset": formset})
