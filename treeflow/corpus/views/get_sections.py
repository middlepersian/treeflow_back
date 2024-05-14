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
    return render(request, "sections_list.html", {"sections": sections})

def get_section_data(request, section_id):
    logger.debug(f"Received section_id: {section_id}")  
    try:
        # Fetch the section and its child sections
        section = Section.objects.get(id=section_id)
        child_sections = Section.objects.filter(container__id=section_id).values('id', 'identifier', 'type')
        
        # Fetch tokens for the section
        tokens = list(section.tokens.values_list('id', flat=True))
        
        # Prepare the response data
        data = {
            'child_sections': list(child_sections),
            'tokens': tokens
        }
        return JsonResponse(data, safe=False)
    except Section.DoesNotExist:
        return JsonResponse({'error': 'Section not found'}, status=404)
    
def get_tokens_for_section(request, section_id):
    try:
        section = Section.objects.get(id=section_id)
    except Section.DoesNotExist:
        return JsonResponse({'error': 'Section not found'}, status=404)

    tokens = section.tokens.values_list('id', flat=True)
    return JsonResponse({'tokens': list(tokens)})    