from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from treeflow.corpus.forms.line_form import SectionLineForm
from treeflow.corpus.models.section import Section
from treeflow.corpus.models.token import Token
from treeflow.corpus.models.section import SectionToken  
import logging

logger = logging.getLogger(__name__)

def line_form_view(request, token_id=None):
    logger.info("Handling request for token_id: %s", token_id)
    
    # Fetch the token or return a 404 if not found
    token = get_object_or_404(Token, pk=token_id) if token_id else None

    # Check if the token has any 'line' type sections associated with it
    line_sections = SectionToken.objects.filter(token=token, section__type='line').select_related('section')
    line = line_sections.first().section if line_sections.exists() else None
    lines = [line] if line else []

    if request.method == 'POST':
        logger.info("POST request received for token_id: %s", token_id)
        return handle_post_request(request, token, line)
    else:
        logger.info("GET request received for token_id: %s", token_id)
        return handle_get_request(request, token, line, lines)

def handle_post_request(request, token, line):
    form = SectionLineForm(request.POST, instance=line)
    if form.is_valid():
        # If a line already exists, update it, otherwise create a new one
        if not line:
            line = Section(type='line')
            line.save()
            SectionToken.objects.create(token=token, section=line)
        form.save()

        # Refresh the token instance from the database
        token.refresh_from_db()

        # Prepare and return the response
        context = {
            'token_id': token.id,
            'line_data': render_to_string('line_data.html', {'token': token}),
        }
        logger.info("Line saved successfully")
        return render(request, 'line_update.html', context)

def handle_get_request(request, token, line, lines):
    form = SectionLineForm(instance=line)
    return render(request, 'line_form.html', {'form': form, 'token': token, 'lines': lines})