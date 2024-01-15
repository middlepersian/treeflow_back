from django.forms import modelformset_factory
from django import forms
from .models import SearchCriteria, ResultFilter

shared_fields = (
    "query",
    "query_type",
    "query_field",
    "is_root",
    "language",
    "case_sensitive",
)


class DistanceForm(forms.ModelForm):
    class Meta:
        model = SearchCriteria
        fields = (
            *shared_fields,
            "distance",
            "distance_type",
        )


class LogicalForm(forms.ModelForm):
    class Meta:
        model = SearchCriteria
        fields = (
            *shared_fields,
            "logical_operator",
        )


class ResultFilterForm(forms.ModelForm):
    class Meta:
        model = ResultFilter
        fields = (
            "text",
            "section",
            "remove_stopwords",
        )


DistanceFormSet = modelformset_factory(SearchCriteria, form=DistanceForm, extra=1)

LogicalFormSet = modelformset_factory(SearchCriteria, form=LogicalForm, extra=1)
