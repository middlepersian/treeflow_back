from django import forms
from django.forms import formset_factory
from .models import SearchForm


class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchForm
        fields = [
            "search_input",
            "criteria_value",
            "criteria_scope",
            "lemmas_word",
            "toggle_field",
        ]


SearchFormSet = formset_factory(SearchForm, min_num=1, extra=1)
