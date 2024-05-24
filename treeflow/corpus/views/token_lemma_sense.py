from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from treeflow.corpus.models import Token  # Import the Token model
from treeflow.corpus.forms.token_form import TokenForm  # Import the TokenForm
from treeflow.dict.forms.sense_form import SenseForm
from treeflow.dict.forms.lemma_form import LemmaForm
import logging


logger = logging.getLogger(__name__)


def token_lemma_sense_view(request, token_id=None):
    logger.debug("token_lemma_sense_view")
    logger.debug("token_id: %s", token_id)

    if request.method != 'GET':
        # Optionally, log an error or warning if a POST request is received
        logger.warning("POST request received on a GET-only view.")
        return HttpResponseBadRequest("This view only handles GET requests.")

    token_instance = None
    if token_id:
        logger.debug("token_id provided")
        token_instance = get_object_or_404(Token, id=token_id)
        logger.debug("token_instance: %s", token_instance)

    token_form = TokenForm(instance=token_instance)
    lemma_form = LemmaForm()
    sense_form = SenseForm()

    context = {
        'token_form': token_form, 
        'lemma_form': lemma_form, 
        'sense_form': sense_form,
        'token_id': token_instance.id if token_instance else None
    }
    return render(request, 'token_lemma_sense.html', context)
