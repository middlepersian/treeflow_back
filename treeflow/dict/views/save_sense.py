import logging
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from treeflow.dict.forms.sense_form import SenseForm

# Configure logger
logger = logging.getLogger(__name__)

def save_sense(request):
    if request.method == 'POST':
        form = SenseForm(request.POST)

        if form.is_valid():
            sense = form.save()
            logger.info(f"Sense object with ID {sense.id} was created successfully.")

            # If the request is via HTMX
            if 'HX-Request' in request.headers:
                logger.info("HTMX request for sense creation.")
                new_form = SenseForm()  # Return a new, empty form
                return render(request, 'sense_form.html', {'sense_form': new_form})
            else:
                # Handle non-HTMX request if necessary
                logger.info("Non-HTMX request for sense creation.")
                # return redirect('some_view')

        else:
            logger.error(f"Form errors: {form.errors}")
            if 'HX-Request' in request.headers:
                logger.info("HTMX request with form errors.")
                # Return the form with errors for HTMX requests
                return render(request, 'sense_form.html', {'sense_form': form})
            else:
                # Handle non-HTMX request with form errors if necessary
                logger.info("Non-HTMX request with form errors.")
                # return render(request, 'your_template_with_errors.html', {'form': form})

    else:
        logger.warning("Received non-POST request on save_sense view.")
        return HttpResponseBadRequest()

    return HttpResponseBadRequest("Invalid request method.")
