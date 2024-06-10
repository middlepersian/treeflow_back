from django.http import JsonResponse
from django.shortcuts import render
from treeflow.corpus.models import Section

import logging
logger = logging.getLogger(__name__)

def get_sections_by_type(request):
    
    text_id = request.GET.get('textId')
    section_type = request.GET.get('sectionTypeSelector')

    logger.debug(f"Received textId: {text_id}")
    logger.debug(f"Received sectionType: {section_type}")

    sections = Section.objects.filter(text_id=text_id, type=section_type)
    return render(request, "section_list.html", {"sections": sections})


def fetch_nested_sections(section_id):
    """Recursively fetch child sections."""
    #section = Section.objects.get(id=section_id)
    #logger.debug(f"Fetching nested sections for section: {section.identifier}")
    logger.debug(f"Fetching nested sections for section_id: {section_id}")
    child_sections = Section.objects.filter(container__id=section_id)
    nested_sections = []
    for child in child_sections:
        nested_child = fetch_nested_sections(child.id)
        nested_sections.append({
            'id': child.id,
            'identifier': child.identifier,
            'type': child.type,
            'child_sections': nested_child  # Include nested child sections
        })
    return nested_sections

def get_section_data(request, section_id):
    logger.debug(f"Received section_id: {section_id}")
    # Fetch the section and its nested child sections
    nested_sections = fetch_nested_sections(section_id)
    
    
    # Prepare the response data
    context = {
        'child_sections': nested_sections,
    }
    return render(request, 'section_data.html', context)

def get_tokens_for_section(request, section_id):
    try:
        section = Section.objects.get(id=section_id)
    except Section.DoesNotExist:
        return JsonResponse({'error': 'Section not found'}, status=404)

    tokens = section.tokens.values_list('id', flat=True)
    return JsonResponse({'tokens': list(tokens)})    