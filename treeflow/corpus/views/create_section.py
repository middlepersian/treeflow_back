# views.py
from django.shortcuts import render, get_object_or_404
from treeflow.corpus.forms.section_form import SectionForm
from treeflow.corpus.models import Token  # Import the Token model
from django.http import JsonResponse
import logging
import uuid

logger = logging.getLogger(__name__)

def create_section_view(request):
    logger.debug("Received request to create a new section")
    if request.method == 'POST':
        logger.debug("Received POST request with data: %s", request.POST)
        form = SectionForm(request.POST)

        if form.is_valid():
            logger.debug("Form is valid. Processing selected tokens...")
            
            # Process the selected tokens field
            token_ids_str = form.cleaned_data['selected_tokens']
            token_ids = token_ids_str.split(',')
            token_uuids = [uuid.UUID(token_id) for token_id in token_ids]
            logger.debug("Processed token UUIDs: %s", token_uuids)

            # Save the section
            section = form.save()

            # Fetch token instances and associate them with the section
            for token_uuid in token_uuids:
                token = get_object_or_404(Token, id=token_uuid)
                section.tokens.add(token)
            logger.debug("Associated tokens with section")

            # Redirecting to referrer URL
            referrer_url = request.POST.get('referrerUrl', '/')
            logger.debug("Redirecting to referrer URL: %s", referrer_url)
            return JsonResponse({'redirect': referrer_url})
        else:
            # Handle form errors
            logger.error("Form is invalid. Errors: %s", form.errors)
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = SectionForm()

    return render(request, 'section_modal.html', {'form': form})
