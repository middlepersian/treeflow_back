import logging
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render
from treeflow.corpus.forms.section_editor_form import SectionEditorForm  
from treeflow.corpus.models import Section
from django.template.loader import render_to_string

# Configure logger
logger = logging.getLogger(__name__)

def save_section_view(request, section_id=None):
    # Initialize the form with the section data if section_id is provided
    if section_id:
        try:
            section = Section.objects.get(id=section_id)
            form = SectionEditorForm(request.POST or None, instance=section)
        except Section.DoesNotExist:
            logger.error(f"Section with ID {section_id} does not exist.")
            return HttpResponseNotFound("Section not found.")
    else:
        form = SectionEditorForm(request.POST or None)

    if request.method == 'POST':
        logger.debug("POST")

        if form.is_valid():
            logger.debug("Form is valid.")
            section = form.save()
            logger.debug(f"Section object with ID {section.id} was created/updated successfully.")
            # Refresh the section instance from the database
            section.refresh_from_db()
            # Prepare and return the response

            context = {
                'section_id': section.id,
                'section_sense_data': render_to_string('section_sense_data.html', {'section': section}),
                # Add other context data as needed
            }
            return render(request, 'section_update.html', context)
        else:
            logger.info("Non-HTMX request with invalid form.")
            # Handle invalid form (e.g., return form errors)

    else:
        logger.warning("Received non-POST request on save_section view.")
        return HttpResponseBadRequest()

    return HttpResponseBadRequest("Invalid request method.")
