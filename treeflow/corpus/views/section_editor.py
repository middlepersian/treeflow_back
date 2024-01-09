from django.shortcuts import render, redirect, get_object_or_404
from treeflow.corpus.models import Section
from treeflow.corpus.forms.section_editor_form import SectionEditorForm
from treeflow.dict.forms.sense_form import SenseForm  # Import the SenseForm
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

    sense_form = SenseForm()  # Create an instance of SenseForm

    return render(request, 'section_editor_form.html', {'form': form, 'sense_form': sense_form, 'section_id': section_id})
