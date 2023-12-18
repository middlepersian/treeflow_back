from django.shortcuts import render, redirect, get_object_or_404
from treeflow.corpus.models import Section, Token  # Import the Token model
from treeflow.corpus.forms.section_editor_form import SectionEditorForm
from treeflow.corpus.forms.token_form import TokenForm  # Import the TokenForm
from treeflow.dict.forms.sense_form import SenseForm
import logging

logger = logging.getLogger(__name__)

def token_sense_view(request, token_id=None):
    logger.debug("token_sense_view")
    logger.debug("token_id: %s" % token_id)

    if token_id:
        token = get_object_or_404(Token, id=token_id)
        token_form = TokenForm(request.POST or None, instance=token, token=token)
    else:
        token_form = TokenForm(request.POST or None)

    sense_form = SenseForm(request.POST or None)  # Initialize SenseForm with POST data if present

    if request.method == 'POST':
        if 'submit_token' in request.POST and token_form.is_valid():
            token_form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
        elif 'submit_sense' in request.POST and sense_form.is_valid():
            sense_form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))

    context = {'token_form': token_form, 'sense_form': sense_form}
    return render(request, 'token_sense.html', context)
