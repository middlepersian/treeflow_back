from django import forms
from treeflow.corpus.models import BibEntry

class BibEntryForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = BibEntry
