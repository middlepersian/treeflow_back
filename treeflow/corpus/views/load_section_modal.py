from treeflow.corpus.forms.section_form import SectionForm
from django.shortcuts import render
import logging
logger = logging.getLogger(__name__)

def load_section_modal(request):
    selected_tokens = request.GET.get('tokens', '')
    text_id = request.GET.get('text_id') 
    logger.debug("Received text_id: %s", text_id)  
    logger.debug("Received selected_tokens: %s", selected_tokens)
    form = SectionForm(initial={'selected_tokens': selected_tokens}, text_id=text_id)
    return render(request, 'section_modal.html', {'form': form})