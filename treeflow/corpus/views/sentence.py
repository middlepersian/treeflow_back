from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.core.cache import cache
from treeflow.corpus.models import Source

import logging
from treeflow.corpus.models import Section

logger = logging.getLogger(__name__)


@login_required
def sentence_view(request, sentence_id):
    # Cache manuscripts for quick access
    cache_key_manuscripts = "manuscripts"
    manuscripts = cache.get(cache_key_manuscripts)

    if manuscripts is None:
        logger.info("Cache miss for manuscripts - Fetching manuscripts from database.")
        manuscripts = Source.objects.filter(type="manuscript").order_by("identifier")
        cache.set(cache_key_manuscripts, manuscripts)
        logger.info("Manuscripts cached for quick access")
    else:
        logger.info("Manuscripts already cached")


    try:
        sentence = Section.objects.get(id=sentence_id)
    except Section.DoesNotExist:
        logger.error("Invalid sentence_id or sentence not found in text")
        raise Http404("Sentence not found")
    
    # get the first token of the sentence
    first_token = sentence.tokens.first()
    # get the image of the first token
    if first_token and first_token.image:
        first_token_image = first_token.image
    else:
        first_token_image = None

    context = {"sentence": sentence, "manuscript_image": first_token_image, "manuscripts": manuscripts}

    return render(request, "sentence.html", context)
