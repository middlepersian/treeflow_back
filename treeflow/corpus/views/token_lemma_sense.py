from django.shortcuts import render, redirect, get_object_or_404
from treeflow.corpus.models import Section, Token  # Import the Token model
from treeflow.corpus.forms.section_editor_form import SectionEditorForm
from treeflow.corpus.forms.token_form import TokenForm  # Import the TokenForm
from treeflow.dict.forms.sense_form import SenseForm
from treeflow.dict.forms.lemma_form import LemmaForm
import logging
from django.db import transaction


logger = logging.getLogger(__name__)

def token_lemma_sense_view(request, token_id=None):
    logger.debug("token_sense_view")
    logger.debug("token_id: %s", token_id)

    if request.method == 'GET':
        logger.debug("GET")

        if token_id:
            token = get_object_or_404(Token, id=token_id)
            token_form = TokenForm(instance=token, token=token)
        else:
            token_form = TokenForm()

        lemma_form = LemmaForm()
        sense_form = SenseForm()  

        lemma_form.fields['related_senses'].label = "Related sensess"
        
    context = {'token_form': token_form, 'lemma_form': lemma_form, 'sense_form': sense_form}
    return render(request, 'token_lemma_sense.html', context)

