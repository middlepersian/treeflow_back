from django import forms
from django.forms import inlineformset_factory
from treeflow.corpus.models import Token, Feature

class FeatureForm(forms.ModelForm):

    class Meta:
        exclude = ('pos',)  # Exclude the 'pos' field from the feature form
        fields = ['feature', 'feature_value']

# Create an inline formset factory
FeatureFormSet = inlineformset_factory(Token, Feature, form=FeatureForm, extra=4,can_delete=True)
