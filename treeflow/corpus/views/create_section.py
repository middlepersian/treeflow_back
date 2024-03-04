from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from treeflow.corpus.forms.section_form import SectionForm
from treeflow.corpus.models.token import Token
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
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
    text_id = request.POST.get('text_id')
    logger.debug("text_id: %s", text_id)
    form = SectionForm(request.POST, user=request.user, text_id=text_id)

    if form.is_valid():
        return process_valid_form(request, form)
    else:
        logger.error("Form is invalid. Errors: %s", form.errors)
        return JsonResponse({'errors': form.errors}, status=400)

def process_valid_form(request, form):
    section = form.save()
    text_id = request.POST.get('text_id')  # Get the text_id from the form submission
    logger.debug("Redirecting to Text ID: %s", text_id)
    relative_url = reverse('corpus:sections', kwargs={'text_id': text_id})
    response = HttpResponse('')
    response['HX-Redirect'] = relative_url  
    return response
    
def handle_get_request(request):
    text_id = request.GET.get('text_id')
    logger.debug("text_id: %s", text_id)
    form = SectionForm(text_id=text_id)
    context = {
        'form': form,
        'text_id': text_id  # Make sure this is included
    }
    return render(request, 'section_modal.html', context)
