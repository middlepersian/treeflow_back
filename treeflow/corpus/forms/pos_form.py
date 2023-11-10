# forms.py
from django import forms
from django.forms import inlineformset_factory
from treeflow.corpus.models import POS, Token

# POSForm for individual POS entries
class POSForm(forms.ModelForm):
    class Meta:
        model = POS
        fields = ('pos', 'type')  # or any other fields you need

# POSFormSet to manage a collection of POS forms
POSFormSet = inlineformset_factory(
    Token, POS, form=POSForm, 
    fields=('pos', 'type'), extra=1, can_delete=True
)
