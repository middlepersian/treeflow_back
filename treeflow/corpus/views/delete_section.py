from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from treeflow.corpus.models.section import Section

import logging
logger = logging.getLogger(__name__)
@require_POST
@csrf_exempt  # Consider CSRF protection as per your security requirements
def delete_section_view(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    section.delete()
    # Return the section ID in the response
    return JsonResponse({'status': 'success', 'section_id': section_id}, status=200)