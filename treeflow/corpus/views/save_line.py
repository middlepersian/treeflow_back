import logging
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from treeflow.corpus.forms.line_form import CreateLineSectionForm

# Configure logger
logger = logging.getLogger(__name__)

def save_line_view(request):
    if request.method == 'POST':
        form = CreateLineSectionForm(request.POST)

        if form.is_valid():
            line = form.save()
            logger.info(f"Line object with ID {line.id} was created successfully.")

            # If the request is via HTMX
            if 'HX-Request' in request.headers:
                logger.info("HTMX request for line creation.")
                new_form = CreateLineSectionForm()  # Return a new, empty form
                return render(request, 'line_form.html', {'create_form': new_form})
            else:
                # Handle non-HTMX request if necessary
                logger.info("Non-HTMX request for sense creation.")
                # return redirect('some_view')

        else:
            logger.error(f"Form errors: {form.errors}")
            if 'HX-Request' in request.headers:
                logger.info("HTMX request with form errors.")
                # Return the form with errors for HTMX requests
                return render(request, 'line_form.html', {'line_form': form})
            else:
                # Handle non-HTMX request with form errors if necessary
                logger.info("Non-HTMX request with form errors.")

    else:
        logger.warning("Received non-POST request on save_sense view.")
        return HttpResponseBadRequest()

    return HttpResponseBadRequest("Invalid request method.")
