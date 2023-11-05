# forms.py
from django import forms
from treeflow.corpus.models.token import Token

class TokenForm(forms.ModelForm):
    class Meta:
        model = Token
        fields = ['transcription', 'transliteration']
