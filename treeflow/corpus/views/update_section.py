from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from treeflow.corpus.models.section import Section
from treeflow.corpus.forms.section_edit_display_tokens import SectionForm
import logging

logger = logging.getLogger(__name__)


def update_section_view(request, section_id=None):
    section = get_object_or_404(Section, id=section_id) if section_id else None
    if request.method == "POST":
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            logger.info("Section updated successfully")
            return JsonResponse({"status": "success", "message": "Section updated successfully"})
        else:
            logger.error("Form is not valid: %s", form.errors)
            return JsonResponse({"status": "error", "message": "Form is not valid", "errors": form.errors}, status=400)
    else:  # GET request
        form = SectionForm(instance=section)
        context = {"form": form, "section": section, "edit_mode": bool(section_id)}
        return render(request, "section_modal.html", context)