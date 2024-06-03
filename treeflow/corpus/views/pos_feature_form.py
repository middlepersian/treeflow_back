from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from treeflow.corpus.forms import POSFormSet, FeatureFormSet
from treeflow.corpus.models import Token, POS, Feature
import logging
import json

logger = logging.getLogger(__name__)


def pos_feature_form(request, token_id=None):
    try:
        if not token_id:
            raise Http404("Token ID not provided")

        token = get_object_or_404(Token, id=token_id)

        # Initialize formset
        pos_formset = POSFormSet(request.POST or None, instance=token, queryset=POS.objects.filter(token=token))
        feature_formset = FeatureFormSet(request.POST or None, instance=token,
                                         queryset=Feature.objects.filter(token=token))

        # log the existing POS and Feature instances
        logger.info(f"POS instances: {pos_formset.queryset}")
        logger.info(f"Feature instances: {feature_formset.queryset}")

        if request.method == 'POST':
            if pos_formset.is_valid() and feature_formset.is_valid():
                # Handle deletions and saves
                for form in pos_formset:
                    if form.cleaned_data.get('DELETE', False) and form.instance.pk:
                        logger.info(f"Deleting POS instance: {form.instance}")
                        form.instance.delete()
                    elif form.has_changed() and form.cleaned_data:
                        # Check for non-empty data in critical fields
                        if 'pos' in form.cleaned_data and form.cleaned_data['pos']:
                            logger.info(f"Saving POS instance: {form.instance}")
                            form.save()
                        else:
                            logger.info("Skipping save for empty or invalid POS form")
                # Save or delete Feature instances
                for form in feature_formset:
                    if form.cleaned_data.get('DELETE', False) and form.instance.pk:
                        logger.info(f"Deleting Feature instance: {form.instance}")
                        form.instance.delete()
                    elif form.has_changed() and form.cleaned_data:
                        if 'feature' in form.cleaned_data and form.cleaned_data['feature'] and \
                                'feature_value' in form.cleaned_data and form.cleaned_data['feature_value']:
                            logger.info(f"Saving Feature instance: {form.instance}")
                            form.save()
                        else:
                            logger.info("Skipping save for empty or invalid Feature form")

                # Refresh the token instance from the database
                token.refresh_from_db()

                # Prepare and return the response
                context = {
                    'token_id': token.id,
                    'pos_data': render_to_string('pos_data.html', {'token': token}),
                    'features_data': render_to_string('feature_data.html', {'token': token})
                }
                return render(request, 'pos_feature_update.html', context)

            else:
                # Log form errors if the form is invalid
                logger.error(json.dumps(pos_formset.errors))
                logger.error(json.dumps(feature_formset.errors))
                return JsonResponse({'status': 'error'}, status=400)

        # Re-fetch or refresh the token instance before rendering the initial form
        token.refresh_from_db()
        # Return the initial form
        return render(request, 'pos_feature_form.html', {
            'pos_formset': pos_formset,
            'feature_formset': feature_formset,
            'token': token
        })

    except Exception as e:
        logger.error(f"Error in pos_feature_form: {str(e)}")
        raise
