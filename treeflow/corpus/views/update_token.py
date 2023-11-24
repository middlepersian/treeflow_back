import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from treeflow.corpus.models import Token

# Set up logging
logger = logging.getLogger(__name__)

def update_token(request, token_id):
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Token ID: {token_id}")
    try:
        token = get_object_or_404(Token, pk=token_id)

        if request.method == 'POST':
            for field in request.POST:
                if field in ['transcription', 'transliteration', 'pos']:  # Add other fields as needed
                    # Log the field being updated
                    logger.info(f"Updating {field} for token with ID {token_id}")

                    setattr(token, field, request.POST[field])
                    token.save(update_fields=[field])
                    return JsonResponse({'status': 'success', 'message': f'{field} updated successfully'})
            
            # Log if no matching field found
            logger.warning(f"No matching field found in POST data for token ID {token_id}")
            return JsonResponse({'status': 'error', 'message': 'No matching field found'})

        # Log if not a POST request
        logger.warning(f"Received a non-POST request for token ID {token_id}")
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})

    except Exception as e:
        # Log the exception details
        logger.error(f"Error in updating token: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'An error occurred during update'})
