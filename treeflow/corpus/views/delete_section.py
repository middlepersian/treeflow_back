from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from treeflow.corpus.models.section import Section


@require_POST
@csrf_exempt  # Consider CSRF protection as per your security requirements
def delete_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    section.delete()
    return JsonResponse({"status": "success"}, status=200)  # Return JSON response
