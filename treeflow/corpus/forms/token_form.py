from django import forms
from treeflow.dict.forms.widgets import SenseWidget, LemmaWidget
from treeflow.corpus.models.token import Token
from treeflow.dict.models import Lemma, Sense

class TokenForm(forms.ModelForm):

    class Meta:
        model = Token
        fields = ['transcription', 'transliteration', 'lemmas', 'senses']
        widgets = {
            'lemmas': LemmaWidget,  # Assign LemmaWidget to 'lemmas' field
            'senses': SenseWidget,  # Assign SenseWidget to 'senses' field
        }

    def __init__(self, *args, **kwargs):
        token = kwargs.pop('token', None)
        super(TokenForm, self).__init__(*args, **kwargs)

        self.fields['transcription'].widget.attrs.update({
            'style': 'max-height: 200px; resize: vertical; width: 100%; border-radius: 5px;',
        })
        self.fields['transliteration'].widget.attrs.update({
            'style': 'max-height: 200px; resize: vertical; width: 100%; border-radius: 5px;',
        })
