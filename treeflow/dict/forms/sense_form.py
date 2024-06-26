from django import forms
from treeflow.dict.forms.widgets import SenseWidget
from treeflow.dict.models import Sense

class SenseForm(forms.ModelForm):
    class Meta:
        model = Sense
        widgets = {
            'related_senses': SenseWidget(attrs={'id': 'sense_related_senses'}),
        }
        fields = ['sense', 'language', 'lemma_related', 'related_senses']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['sense'].widget.attrs.update({
            'placeholder': 'Enter sense here...',
            'style': 'max-height: 200px; resize: vertical; width: 100%; border-radius: 5px;',
        })
        self.fields['language'].widget.attrs.update({
            'style': 'border-radius: 5px;',
        })