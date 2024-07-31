from django.shortcuts import get_object_or_404, render

from treeflow.corpus.models.section import Section


def render_info_modal(request):
    """
    Render the info modal for a section.
    """
    
    section_id = request.GET.get("section_id", "")
    section = get_object_or_404(Section.objects.prefetch_related("tokens", "tokens__section_tokens", "tokens__pos_token", "tokens__feature_token", "tokens__senses"), id=section_id)

    context = {
        "section": section,
    }

    return render(request, "search/section_info_modal.html", context)