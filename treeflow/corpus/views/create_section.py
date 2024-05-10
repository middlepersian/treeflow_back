from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from treeflow.corpus.forms.section_form import SectionForm
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
import logging

logger = logging.getLogger(__name__)

@login_required
def create_section_view(request):
    if request.method == 'POST':
        return handle_post_request(request)
    return handle_get_request(request)

def handle_post_request(request):
    form = SectionForm(request.POST, user=request.user, text_id=request.POST.get('text_id'))
    if form.is_valid():
        section = form.save()
        return HttpResponse('', headers={'HX-Redirect': reverse('corpus:sections', kwargs={'text_id': section.text_id})})
    return JsonResponse({'errors': form.errors}, status=400)

def handle_get_request(request):
    form = SectionForm(text_id=request.GET.get('text_id'))
    return render(request, 'section_modal.html', {'form': form, 'text_id': form.text_id})