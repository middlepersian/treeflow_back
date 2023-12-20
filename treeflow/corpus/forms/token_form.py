# forms.py
from django import forms
from treeflow.corpus.models.token import Token
from treeflow.dict.models import Lemma, Sense

class TokenForm(forms.ModelForm):
    lemmas = forms.ModelMultipleChoiceField(
        queryset=Lemma.objects.none(),  # Default to none, will be set in __init__
        required=False
    )
    senses = forms.ModelMultipleChoiceField(
        queryset=Sense.objects.none(),  # Default to none, will be set in __init__
        required=False
    )

    class Meta:
        model = Token
        fields = ['transcription', 'transliteration', 'lemmas', 'senses']

    def __init__(self, *args, **kwargs):
        token = kwargs.pop('token', None)  # Get the token instance from kwargs
        super(TokenForm, self).__init__(*args, **kwargs)
        
        if token:  # If a token instance is provided, set the queryset for lemmas and senses
            self.fields['lemmas'].queryset = token.lemmas.all()
            self.fields['senses'].queryset = token.senses.all()