from django.core.cache import cache
from django.shortcuts import render
from treeflow.corpus.forms.text_form import TextForm
from treeflow.datafeed.cache import cache_all_texts 
import logging

logger = logging.getLogger(__name__)

def texts_view(request):
    cache_key_texts = "all_texts"
    texts = cache.get(cache_key_texts)

    if not texts:
        logger.info("Cache miss for texts - Fetching texts from database.")
        cache_all_texts()
        logger.info("Cache miss for texts - Triggered Huey task to update cache.")
        texts = cache.get(cache_key_texts)
        logger.info("Cache miss for texts - Texts have been updated in the cache.")

    logger.debug("request method: %s", request.method)

    form = TextForm()

    context = {'texts': texts, 'form': form}
    return render(request, 'texts.html', context)
