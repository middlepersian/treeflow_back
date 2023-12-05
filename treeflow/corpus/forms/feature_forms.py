from django import forms
from django.forms import inlineformset_factory
from treeflow.corpus.models import Token, Feature

class FeatureForm(forms.ModelForm):
    id = forms.ModelChoiceField(queryset=Feature.objects.all(), widget=forms.HiddenInput())

    class Meta:
        exclude = ('pos',)  # Exclude the 'pos' field from the feature form
        fields = ['feature', 'feature_value']

# Create an inline formset factory
FeatureFormSet = inlineformset_factory(Token, Feature, form=FeatureForm, extra=2, can_delete=True)
