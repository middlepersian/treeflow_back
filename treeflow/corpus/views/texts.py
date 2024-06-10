from django.core.cache import cache
from django.shortcuts import render
from treeflow.corpus.forms.text_form import TextForm
from treeflow.datafeed.cache import cache_all_texts 
import logging
from django.urls import reverse
from django.middleware.csrf import get_token
from treeflow.corpus.forms.text_genre_form import TextGenreForm

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
    csrf_token = get_token(request)

    text_forms = []
    for text in texts:
        genre_form = TextGenreForm(
            initial={'label': text.label if text.label is not None else 'None'},
            hx_post_url=reverse('corpus:update_text', kwargs={'text_id' : text.id}),
            csrf_token=csrf_token,
        )
        text_forms.append((text, genre_form))

    context = {'text_forms': text_forms, 'form': form}
    return render(request, 'texts.html', context)
