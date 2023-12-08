import logging
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from treeflow.corpus.models import Token, POS

# Set up logging
logger = logging.getLogger(__name__)


def update_token(request, token_id):
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Token ID: {token_id}")
    try:
        token = get_object_or_404(Token, pk=token_id)

        if request.method == 'POST':
            # Handling pos updates separately
            if 'pos' in request.POST:
                pos_value = request.POST['pos']
                logger.info(f"Updating pos for token with ID {token_id} to {pos_value}")
                # Create or update the POS instance associated with the token
                pos_instance, created = POS.objects.update_or_create(
                    token=token,
                    defaults={'pos': pos_value}
                )
                # Render the updated dropdown
                updated_dropdown_html = render_to_string('pos_dropdown.html', {
                    'token': token,
                    'pos_choices': POS.objects.order_by('pos').values_list('pos', flat=True).distinct()
                }).replace('\n', '').replace('\r', '')
                return HttpResponse(updated_dropdown_html)

            # Handling other fields
            for field in ['transcription', 'transliteration', 'number_in_sentence']:
                if field in request.POST:
                    logger.info(f"Updating {field} for token with ID {token_id}")
                    setattr(token, field, request.POST[field])
                    token.save(update_fields=[field])
                    return JsonResponse({'status': 'success', 'message': f'{field} updated successfully'})
                else:
                    logger.info(f"Field {field} not provided in POST data for token ID {token_id}")

            # If no recognized fields are found
            logger.warning(f"No matching field found in POST data for token ID {token_id}")
            return JsonResponse({'status': 'error', 'message': 'No matching field found'})

        else:
            logger.warning(f"Received a non-POST request for token ID {token_id}")
            return JsonResponse({'status': 'error', 'message': 'Invalid request'})

    except Exception as e:
        logger.error(f"Error in updating token: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'An error occurred during update'})
