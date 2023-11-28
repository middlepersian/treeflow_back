from django.shortcuts import redirect
from treeflow.corpus.models import Token, Feature
from treeflow.corpus.forms.feature_forms import FeatureFormSet


def update_features(request, token_id):
    token = Token.objects.get(pk=token_id)
    formset = FeatureFormSet(request.POST, instance=token)

    if formset.is_valid():
        formset.save()
        # Redirect or update the page
    else:
        pass

    # Redirect to the tokens page or appropriate URL
    return redirect('treeflow.corpus:tokens')
