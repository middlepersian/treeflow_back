from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from treeflow.corpus.forms.text_form import TextForm
from treeflow.corpus.models import Text
from treeflow.datafeed.tasks import cache_all_texts  # Import the Celery task

import logging

logger = logging.getLogger(__name__)

def texts_view(request):
    cache_key_texts = "all_texts"
    texts = cache.get(cache_key_texts)

    if not texts:
        logger.info("Cache miss for texts - Fetching texts from database.")
        cache_all_texts.apply()  # Trigger the Celery task to update cache
        logger.info("Cache miss for texts - Triggered Celery task to update cache.")
        texts = cache.get(cache_key_texts)

    logger.debug("request method: %s", request.method)

    if request.method == 'POST':
        text_id = request.POST.get('text_id')
        logger.debug("text_id: %s", text_id)
        if text_id:
            text = get_object_or_404(Text, pk=text_id)
            form = TextForm(request.POST, instance=text)
        else:
            form = TextForm(request.POST)

        if form.is_valid():
            saved_text = form.save()
            cache.delete(cache_key_texts)  # Invalidate cache
            if request.headers.get('HX-Request'):
                html = render_to_string('text_row.html', {'text': saved_text})
                return JsonResponse({'html': html})
        else:
            pass

    else:
        form = TextForm()

    context = {'texts': texts, 'form': form}
    return render(request, 'texts.html', context)
