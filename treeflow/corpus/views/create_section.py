# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from treeflow.corpus.forms.section_form import SectionForm
from treeflow.corpus.models.token import Token
from django.http import JsonResponse
import logging
import uuid

logger = logging.getLogger(__name__)


@login_required
def create_section_view(request):
    try:
        if request.method == 'POST':
            return handle_post_request(request)
        else:
            return handle_get_request(request)
    except Exception as e:
        logger.error("An error occurred in create_section_view: %s", e)
        return JsonResponse({'error': 'Internal Server Error'}, status=500)


def handle_post_request(request):
    logger.debug("Received POST request with data: %s", request.POST)
    text_id = request.POST.get('text_id')
    form = SectionForm(request.POST, text_id=text_id, user=request.user)

    if form.is_valid():
        return process_valid_form(form)
    else:
        logger.error("Form is invalid. Errors: %s", form.errors)
        return JsonResponse({'errors': form.errors}, status=400)


def process_valid_form(form):
    logger.debug("Form is valid. Processing selected tokens...")
    token_ids_str = form.cleaned_data['selected_tokens']
    token_ids = token_ids_str.split(',')
    token_uuids = [uuid.UUID(token_id) for token_id in token_ids]
    logger.debug("Processed token UUIDs: %s", token_uuids)

    section = form.save()
    for token_uuid in token_uuids:
        try:
            token = get_object_or_404(Token, id=token_uuid)
            section.tokens.add(token)
        except Exception as e:
            logger.error("Error adding token with UUID %s: %s", token_uuid, e)

    logger.debug("Associated tokens with section")
    referrer_url = request.POST.get('referrerUrl', '/')
    logger.debug("Redirecting to referrer URL: %s", referrer_url)
    return JsonResponse({'redirect': referrer_url})


def handle_get_request(request):
    text_id = request.GET.get('text_id')
    logger.debug("Received GET request with text_id: %s", text_id)
    form = SectionForm(text_id=text_id)
    return render(request, 'section_modal.html', {'form': form})