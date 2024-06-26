import logging
from django.http import HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from treeflow.corpus.forms.token_form import TokenForm  
from treeflow.corpus.models import Token
from django.template.loader import render_to_string

# Configure logger
logger = logging.getLogger(__name__)

def save_token(request, token_id=None):
    # Initialize the form with the token data if token_id is provided
    if token_id:
        try:
            token = Token.objects.get(id=token_id)
            form = TokenForm(request.POST or None, instance=token)
        except Token.DoesNotExist:
            logger.error(f"Token with ID {token_id} does not exist.")
            return HttpResponseNotFound("Token not found.")
    else:
        form = TokenForm(request.POST or None)

    if request.method == 'POST':
        logger.debug("POST")

        if form.is_valid():
            logger.debug("Form is valid.")
            token = form.save()
            logger.debug(f"Token object with ID {token.id} was created/updated successfully.")
            # Refresh the token instance from the database
            token.refresh_from_db()
            # Prepare and return the response

            context = {
                'token_id': token.id,
                'transcription_data': render_to_string('transcription_data.html', {'token': token}),
                'transliteration_data': render_to_string('transliteration_data.html', {'token': token}),
                'lemma_data': render_to_string('lemma_data.html', {'token': token}),
                'sense_data': render_to_string('sense_data.html', {'token': token}),
                'gloss_data': render_to_string('gloss_data.html', {'token': token})
            }
            return render(request, 'token_lemma_sense_update.html', context)
        else:
            logger.info("Non-HTMX request with valid form.")
            # Return or handle as necessary

    else:
        logger.warning("Received non-POST request on save_token view.")
        return HttpResponseBadRequest()

    return HttpResponseBadRequest("Invalid request method.")
