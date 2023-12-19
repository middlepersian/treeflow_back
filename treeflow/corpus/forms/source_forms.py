from django import forms
from ..models import Source, BibEntry
from django.forms import modelformset_factory

class BibEntryForm(forms.ModelForm):
    class Meta:
        model = BibEntry
        fields = ['key']

class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['type', 'identifier', 'description','sources', 'references']
        widgets={
            'sources': forms.CheckboxSelectMultiple(),
            'references': forms.CheckboxSelectMultiple()
        }


# Create the Source formset
SourceFormSet = modelformset_factory(Source, form=SourceForm, extra=1)

# Create the BibEntry formset
BibEntryFormSet = modelformset_factory(BibEntry, form=BibEntryForm, extra=1)

class SourceSourcesForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('sources',)
        widgets = {
            'sources': forms.CheckboxSelectMultiple()
        }