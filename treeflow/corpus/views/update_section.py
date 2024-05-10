from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from treeflow.corpus.models.section import Section
from treeflow.corpus.forms.section_form import SectionForm
import logging

logger = logging.getLogger(__name__)

def update_section_view(request, section_id):
    if not section_id:
        logger.error("No section ID provided")
        return JsonResponse({'status': 'error', 'message': 'No section ID provided'}, status=400)

    section = get_object_or_404(Section, id=section_id)

    if request.method != 'POST':
        logger.error("Invalid request method")
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

    form = SectionForm(request.POST, instance=section)
    if form.is_valid():
        form.save()
        logger.info('Section updated successfully')
        return JsonResponse({'status': 'success', 'message': 'Section updated successfully'})
    
    logger.error('Form is not valid: %s', form.errors)
    return JsonResponse({'status': 'error', 'message': 'Form is not valid', 'errors': form.errors}, status=400)