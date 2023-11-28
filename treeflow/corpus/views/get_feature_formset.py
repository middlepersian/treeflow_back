from django.shortcuts import redirect, render
from treeflow.corpus.models import Token, Feature
from treeflow.corpus.forms.feature_forms import FeatureFormSet

def get_feature_formset(request, token_id):
    token = Token.objects.get(pk=token_id)
    formset = FeatureFormSet(instance=token)
    return render(request, 'feature_formset.html', {'formset': formset})
