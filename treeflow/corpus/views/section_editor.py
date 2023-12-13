from django.shortcuts import render, redirect, get_object_or_404
from treeflow.corpus.models import Section
from treeflow.corpus.forms.section_editor_form import SectionEditorForm
import logging
logger = logging.getLogger(__name__)

def section_editor_form_view(request, section_id=None):
    logger.debug("section_editor_form_view")
    logger.debug("section_id: %s" % section_id)

    if section_id:
        section = get_object_or_404(Section, id=section_id)
        form = SectionEditorForm(request.POST or None, instance=section)
    else:
        form = SectionEditorForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'section_editor_form.html', {'form': form})
