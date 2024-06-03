from django import forms
from django_select2 import forms as s2forms
from treeflow.corpus.models import Section, SectionToken



class SectionSelect2MultipleWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "identifier__icontains",
    ]

class SectionTokenForm(forms.ModelForm):
    section = forms.ModelMultipleChoiceField(
        queryset=Section.objects.filter(type='line'),
        widget=SectionSelect2MultipleWidget
    )

    class Meta:
        model = SectionToken
        fields = ['section']
