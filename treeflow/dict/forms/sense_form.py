from django import forms
from django.forms import inlineformset_factory
from treeflow.dict.forms.widgets import SenseWidget
from treeflow.dict.models import Sense
from treeflow.corpus.models import Section
from django_select2 import forms as s2forms


class SenseForm(forms.ModelForm):
    class Meta:
        model = Sense
        widgets = {
            'related_senses': SenseWidget(attrs={'id': 'sense_related_senses'}),
        }
        fields = ['sense', 'language', 'lemma_related', 'related_senses']
