# forms.py
from django import forms
from django.forms import inlineformset_factory
from django_select2 import forms as s2forms
from treeflow.dict.models import Lemma
from treeflow.dict.forms.widgets import LemmaWidget
from treeflow.dict.forms.widgets import SenseWidget
from treeflow.corpus.models import Token


class LemmaForm(forms.ModelForm):
    class Meta:
        model = Lemma
        fields = ['word', 'language', 'multiword_expression', 'related_lemmas', 'related_senses']
        widgets = {
            'related_lemmas': LemmaWidget,
            'related_senses': SenseWidget(attrs={'id': 'lemma_related_senses'}),        }

