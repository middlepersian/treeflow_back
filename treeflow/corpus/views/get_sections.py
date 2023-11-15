from django.http import JsonResponse
from treeflow.corpus.models import Section

def get_sections_by_type(request, text_id, section_type):
    sections = Section.objects.filter(text=text_id, type=section_type).values('id', 'identifier')
    return JsonResponse(list(sections), safe=False)
