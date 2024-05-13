from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from treeflow.corpus.models.section import Section

import logging
logger = logging.getLogger(__name__)
@require_POST
@csrf_exempt  # Consider CSRF protection as per your security requirements
def delete_section_view(request, section_id):
    logger.info(f"Deleting section {section_id}")
    section = get_object_or_404(Section, id=section_id)
    #get text_id and section_type before deleting the section
    text_id = section.text_id
    section_type = section.type
    section.delete()
    logger.info(f"Section {section_id} found")
    logger.info(f"Section {section_id} deleted successfully")
    sections = Section.objects.filter(text_id=text_id, type=section_type)
    logger.info(f"Sections filtered by text_id {text_id} and section_type {section_type}")
    return render(request, "sections_list.html", {"sections": sections})
