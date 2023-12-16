from django import forms
from django.forms import inlineformset_factory
from treeflow.dict.models import Sense
from treeflow.corpus.models import Section


class SenseForm(forms.ModelForm):
    class Meta:
        model = Sense
        fields = ['sense', 'language', 'lemma_related', 'related_senses']  
