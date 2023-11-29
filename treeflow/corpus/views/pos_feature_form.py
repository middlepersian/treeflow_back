from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from treeflow.corpus.forms import POSFormSet, FeatureFormSet
from treeflow.corpus.models import Token, POS, Feature
import logging

logger = logging.getLogger(__name__)


def pos_feature_form(request, token_id=None):
    try:
        if not token_id:
            raise Http404("Token ID not provided")

        token = get_object_or_404(Token, id=token_id)
        pos_instance = POS.objects.filter(token=token).first()
        pos_formset = POSFormSet(request.POST or None, instance=token, queryset=POS.objects.filter(token=token))
        feature_formset = FeatureFormSet(request.POST or None, instance=token,
                                         queryset=Feature.objects.filter(token=token))

        if request.method == 'POST':
            if pos_formset.is_valid() and feature_formset.is_valid():
                pos_formset.save()
                feature_formset.save()
                context = {
                    'token_id': token.id,  # Pass token ID explicitly
                    'pos_data': render_to_string('pos_data.html', {'token': token}),
                    'features_data': render_to_string('feature_data.html', {'token': token})
                }
                return render(request, 'pos_feature_update.html', context)

            else:
                # Log form errors if the form is invalid
                if not pos_formset.is_valid():
                    logger.error(f"POS Form errors: {pos_formset.errors.as_json()}")
                if not feature_formset.is_valid():
                    logger.error(f"Feature FormSet errors: {feature_formset.errors}")

                return JsonResponse({'status': 'error'}, status=400)

        # Handle GET requests by rendering the full form
        return render(request, 'pos_feature_form.html', {
            'pos_formset': pos_formset,
            'feature_formset': feature_formset,
            'token': token
        })

    except Exception as e:
        logger.error(f"Error in pos_feature_form: {e}")
        raise
