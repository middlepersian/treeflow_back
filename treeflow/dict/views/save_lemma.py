import logging
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from treeflow.dict.forms.lemma_form import LemmaForm

# Configure logger
logger = logging.getLogger(__name__)

def save_lemma(request):
    if request.method == 'POST':
        form = LemmaForm(request.POST)

        if form.is_valid():
            lemma = form.save()
            logger.info(f"Lemma object with ID {lemma.id} was created successfully.")

            # If the request is via HTMX
            if 'HX-Request' in request.headers:
                logger.info("HTMX request for lemma creation.")
                new_form = LemmaForm()  # Return a new, empty form
                return render(request, 'lemma_form.html', {'lemma_form': new_form})
            else:
                # Handle non-HTMX request if necessary
                logger.info("Non-HTMX request for lemma creation.")
                # return redirect('some_view')

        else:
            logger.error(f"Form errors: {form.errors}")
            if 'HX-Request' in request.headers:
                logger.info("HTMX request with form errors.")
                # Return the form with errors for HTMX requests
                return render(request, 'lemma_form.html', {'lemma_form': form})
            else:
                # Handle non-HTMX request with form errors if necessary
                logger.info("Non-HTMX request with form errors.")
                # return render(request, 'your_template_with_errors.html', {'form': form})

    else:
        logger.warning("Received non-POST request on save_lemma view.")
        return HttpResponseBadRequest()

    return HttpResponseBadRequest("Invalid request method.")
