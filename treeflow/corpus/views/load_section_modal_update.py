from django.shortcuts import render, get_object_or_404
import logging
from treeflow.corpus.forms.section_create import SectionForm
from treeflow.corpus.models.section import Section

logger = logging.getLogger(__name__)

def load_section_modal_update(request):
    section_id = request.GET.get('section_id')
    logger.debug("Loading section modal with section_id: %s", section_id)
    selected_tokens = request.GET.get('tokens', '')
    text_id = request.GET.get('text_id')
    logger.debug("Loading section modal with text_id: %s", text_id)

    if section_id:
        section = get_object_or_404(Section, id=section_id)
        token_ids = ','.join(str(token.id) for token in section.tokens.all())
        logger.debug("Editing section with id: %s, token_ids: %s", section_id, token_ids)
        form = SectionForm(section_id=section_id)
        edit_mode = True
    else:
        section = None  # Explicitly set section to None if no section_id
        logger.debug("Creating new section with text_id: %s, selected_tokens: %s", text_id, selected_tokens)
        form = SectionForm(initial={'selected_tokens': selected_tokens}, text_id=text_id)
        edit_mode = False

    context = {
        'form': form,
        'edit_mode': edit_mode,
        'text_id': text_id,
        'section': section  # Pass the section object to the context
    }
    return render(request, 'section_modal_update.html', context)