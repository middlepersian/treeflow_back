import logging
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from treeflow.dict.models import Lemma
from django.template.loader import render_to_string
from django.shortcuts import redirect

# Set up logging
logger = logging.getLogger(__name__)

def update_lemma(request, lemma_id):
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Lemma ID: {lemma_id}")

    try:
        lemma = get_object_or_404(Lemma, pk=lemma_id)

        if request.method == 'POST':
            # Handling lemma fields updates
            for field in ['word', 'language', 'stage']:
                if field in request.POST:
                    new_value = request.POST[field]
                    logger.info(f"Updating {field} for lemma with ID {lemma_id} to {new_value}")
                    setattr(lemma, field, new_value)
            
            # Handling multiword_expression update
            logger.debug(f"Request.POST: {request.POST}")
            if 'multiword_expression' in request.POST:
                new_value = request.POST['multiword_expression'] == 'on'
                logger.info(f"Updating multiword_expression for lemma with ID {lemma_id} to {new_value}")
                lemma.multiword_expression = new_value
            else:
                new_value = False
                logger.info(f"Updating multiword_expression for lemma with ID {lemma_id} to {new_value}")
                lemma.multiword_expression = new_value
            
            # Handling categories update
            if 'categories' in request.POST:
                new_categories = request.POST.getlist('categories')
                logger.info(f"Updating categories for lemma with ID {lemma_id} to {new_categories}")
                lemma.categories = new_categories
            
            lemma.save()

            updated_lemma_html = render_to_string('lemma_details.html', {'lemma': lemma})
            return HttpResponse(updated_lemma_html)

        else:
            logger.warning(f"Received a non-POST request for lemma ID {lemma_id}")
            return JsonResponse({'status': 'error', 'message': 'Invalid request'})

    except Exception as e:
        logger.error(f"Error in updating lemma: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'An error occurred during update'})
