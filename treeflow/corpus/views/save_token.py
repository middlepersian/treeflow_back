import logging
from django.http import HttpResponseBadRequest
from django.shortcuts import render
# Import your TokenForm here
from treeflow.corpus.forms.token_form import TokenForm  # Import the TokenForm

# Configure logger
logger = logging.getLogger(__name__)

def save_token(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)

        if form.is_valid():
            token = form.save()
            # save m2m
            form.save_m2m()
            logger.info(f"Token object with ID {token.id} was created successfully.")

            if 'HX-Request' in request.headers:
                logger.info("HTMX request for token creation.")
                new_form = TokenForm()  # Return a new, empty form
                # Send a custom JSON response
                return JsonResponse({
                    'status': 'success',
                    'message': 'Token saved successfully',
                    'token_id': token.id
                })
            else:
                # Handle non-HTMX request
                logger.info("Non-HTMX request for token creation.")
                # Redirect or handle as necessary
                # return redirect('some_view')

        else:
            logger.error(f"Form errors: {form.errors}")
            if 'HX-Request' in request.headers:
                logger.info("HTMX request with form errors.")
                # Return the form with errors for HTMX requests
                return render(request, 'token_lemma_sense.html', {'token_form': form})
            else:
                # Handle non-HTMX request with form errors
                logger.info("Non-HTMX request with form errors.")
                # Return or handle as necessary
                # return render(request, 'your_template_with_errors.html', {'form': form})

    else:
        logger.warning("Received non-POST request on save_token view.")
        return HttpResponseBadRequest()

    return HttpResponseBadRequest("Invalid request method.")
