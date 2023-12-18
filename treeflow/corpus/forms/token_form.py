from django import forms
from treeflow.corpus.models.token import Token
from treeflow.dict.models import Lemma, Sense
from django_select2 import forms as s2forms

class LemmaWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "lemma__icontains",  # Adjust the field name as per your Lemma model
    ]

class SenseWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "sense__icontains",
    ]

class TokenForm(forms.ModelForm):
    lemmas = forms.ModelMultipleChoiceField(
        queryset=Lemma.objects.none(),
        required=False,
        widget=LemmaWidget,  # Use the custom LemmaWidget here
    )
    senses = forms.ModelMultipleChoiceField(
        queryset=Sense.objects.none(),
        required=False,
        widget=SenseWidget,  # Use the custom SenseWidget here
    )

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
        
        if token:
            self.fields['lemmas'].queryset = token.lemmas.all()
            self.fields['senses'].queryset = token.senses.all()
