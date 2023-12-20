# forms.py
from django import forms
from django.forms import inlineformset_factory
from treeflow.dict.models import Lemma
from treeflow.corpus.models import Token

class LemmaForm(forms.ModelForm):
    class Meta:
        model = Lemma
        fields = ['word']  # fields of Lemma
