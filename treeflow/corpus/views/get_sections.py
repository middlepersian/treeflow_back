from django.http import JsonResponse
from treeflow.corpus.models import Section

def get_sections_by_type(request, text_id, section_type):
    sections = Section.objects.filter(text=text_id, type=section_type).values('id', 'identifier')
    return JsonResponse(list(sections), safe=False)

def get_child_sections(request, section_id):
    child_sections = Section.objects.filter(container__id=section_id).values('id', 'identifier', 'type')
    return JsonResponse(list(child_sections), safe=False)

def get_tokens_for_section(request, section_id):
    try:
        section = Section.objects.get(id=section_id)
    except Section.DoesNotExist:
        return JsonResponse({'error': 'Section not found'}, status=404)

    tokens = section.tokens.values_list('id', flat=True)
    return JsonResponse({'tokens': list(tokens)})