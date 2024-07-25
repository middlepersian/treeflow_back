from django.shortcuts import render

from treeflow.corpus.models.section import Section


def render_info_modal(request):
    """
    Render the info modal for a section.
    """
    
    section_id = request.GET.get("section_id", "")
    section = Section.objects.get(id=section_id)

    context = {
        "section": section,
    }

    return render(request, "search/section_info_modal.html", context)