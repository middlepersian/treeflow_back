from django.http import HttpResponseBadRequest
from django.shortcuts import render
import logging
from treeflow.corpus.forms.section_create import SectionForm
from treeflow.corpus.models import Token

logger = logging.getLogger(__name__)

def load_section_modal_create(request):
    section_id = request.GET.get('section_id')
    selected_token_ids = request.GET.get('tokens', None)
    text_id = request.GET.get('text_id')

    if section_id:
        return HttpResponseBadRequest()
    else:
        if selected_token_ids:
            tokens = Token.objects.filter(id__in=selected_token_ids.split(","))
        else:
            tokens = []
        form = SectionForm(text_id=text_id, selected_tokens=tokens)

    return render(
        request,
        'section_modal_create.html',
        dict(
            form=form,
            text_id=text_id,
            tokens=tokens
        ))
