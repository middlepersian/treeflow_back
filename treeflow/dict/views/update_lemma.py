import logging

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string

from treeflow.dict.models import Lemma
from treeflow.dict.models.sense import Sense

# Set up logging
logger = logging.getLogger(__name__)

def update_lemma(request, lemma_id):
    try:
        lemma = get_object_or_404(Lemma, pk=lemma_id)

        if request.method == 'POST':
            # Handling lemma fields updates
            for field in ['word', 'language', 'stage']:
                if field in request.POST:
                    new_value = request.POST[field]
                    # logger.info(f"Updating {field} for lemma with ID {lemma_id} to {new_value}")
                    setattr(lemma, field, new_value)
            
            # Handling multiword_expression update
            logger.debug(f"Request.POST: {request.POST}")
            if 'multiword_expression' in request.POST:
                new_value = request.POST['multiword_expression'] == 'on'
                # logger.info(f"Updating multiword_expression for lemma with ID {lemma_id} to {new_value}")
                lemma.multiword_expression = new_value
            else:
                new_value = False
                # logger.info(f"Updating multiword_expression for lemma with ID {lemma_id} to {new_value}")
                lemma.multiword_expression = new_value
            
            # Handling categories update
            if 'categories' in request.POST:
                new_categories = request.POST.getlist('categories')
                # logger.info(f"Updating categories for lemma with ID {lemma_id} to {new_categories}")
                lemma.categories = new_categories

            # Handling related senses
            related_sense_ids = request.POST.getlist('related_senses')
            if related_sense_ids.__len__() > 0:
                related_senses = Sense.objects.filter(pk__in=related_sense_ids)
                lemma.related_senses.set(related_senses)
                # logger.info(f"Updated related senses for lemma with ID {lemma_id} to {related_sense_ids}")
            else:
                lemma.related_senses.clear()
                # logger.info(f"Removed all related senses for lemma with ID {lemma_id}")

            # Handling adding related lemmas
            related_lemma_ids = request.POST.getlist('related_lemmas')
            if related_lemma_ids.__len__() > 0:
                related_lemmas = Lemma.objects.filter(pk__in=related_lemma_ids)
                lemma.related_lemmas.set(related_lemmas)
                # logger.info(f"Updated related lemmas for lemma with ID {lemma_id} to {related_lemma_ids}")
            else:
                lemma.related_lemmas.clear()
                # logger.info(f"Removed all related lemmas for lemma with ID {lemma_id}")

            lemma.save()

            updated_lemma_html = render_to_string('lemma_details.html', {'lemma': lemma})
            return HttpResponse(updated_lemma_html)

        else:
            logger.warning(f"Received a non-POST request for lemma ID {lemma_id}")
            return JsonResponse({'status': 'error', 'message': 'Invalid request'})

    except Exception as e:
        logger.error(f"Error in updating lemma: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'An error occurred during update'})
