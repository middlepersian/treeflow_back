# forms.py
from django import forms
from treeflow.dict.models import Lemma
from treeflow.dict.forms.widgets import LemmaWidget
from treeflow.dict.forms.widgets import SenseWidget


class LemmaForm(forms.ModelForm):
    class Meta:
        model = Lemma
        fields = ['word', 'language', 'multiword_expression', 'related_lemmas', 'related_senses']
        widgets = {
            'related_lemmas': LemmaWidget,
            'related_senses': SenseWidget(attrs={'id': 'lemma_related_senses'})}

