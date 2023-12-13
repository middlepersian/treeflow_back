import logging
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from treeflow.corpus.models import Text

# Set up logging
logger = logging.getLogger(__name__)


def update_text(request, text_id):
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Text ID: {text_id}")
    try:
        text = get_object_or_404(Text, pk=text_id)
        logger.debug(f"Text: {text}")

        if request.method == 'POST':

            # Handling default fields
            for field in ['title', 'identifier', 'series', 'label', 'version', 'stage']:
                if field in request.POST:
                    logger.info(f"Updating {field} for text with ID {text_id}")
                    setattr(text, field, request.POST[field])
                    text.save(update_fields=[field])
                    return JsonResponse({'status': 'success', 'message': f'{field} updated successfully'})
                else:
                    logger.info(f"Field {field} not provided in POST data for text ID {text_id}")

            # If no recognized fields are found
            logger.warning(f"No matching field found in POST data for text ID {text_id}")
            return JsonResponse({'status': 'error', 'message': 'No matching field found'})

        else:
            logger.warning(f"Received a non-POST request for text ID {text_id}")
            return JsonResponse({'status': 'error', 'message': 'Invalid request'})

    except Exception as e:
        logger.error(f"Error in updating text: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'An error occurred during update'})
