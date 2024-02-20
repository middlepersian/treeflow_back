from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.core.cache import cache
from django.shortcuts import render
from django.db.models import Prefetch
from treeflow.corpus.models import Section, SectionToken, Token
from treeflow.datafeed.tasks import cache_all_texts

import logging

logger = logging.getLogger(__name__)

@login_required
def sentences_view(request, text_id=None):
    logger.info('text_id : %s', text_id)

    # Fetching or caching texts
    cache_key_texts = "all_texts"
    texts = cache.get(cache_key_texts)
    if texts is None:
        logger.info("Cache miss for texts - Fetching texts from database.")
        cache_all_texts.delay()  # Non-blocking call to update cache
        texts = []  # Fallback if cache is still empty

    selected_text_id = text_id if text_id else request.GET.get('text_id')

    # Building the cache key for sentences
    cache_key_sentences = f"sentences_{selected_text_id}"
    sentences = cache.get(cache_key_sentences)

    if sentences is None:
        logger.info("Cache miss for sentences - Fetching from database.")
        sentences = Section.objects.filter(type='sentence', text=selected_text_id) \
            .prefetch_related(
                Prefetch(
                    'sectiontoken_set',
                    queryset=SectionToken.objects.filter(section__type='line').select_related('section'),
                    to_attr='line_sections'
                ),
                Prefetch(
                    'tokens',
                    queryset=Token.objects.select_related('image')
                    .prefetch_related('pos_token', 'feature_token', 'lemmas', 'senses', 'comment_token')
                ),
                'senses'  # Prefetch the many-to-many field 'senses'
            )
        cache.set(cache_key_sentences, sentences, 300)


    # Paginator setup
    paginator = Paginator(sentences, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'texts': texts,
        'selected_text_id': selected_text_id or '',
        'page_obj': page_obj,
        'current_view': 'corpus:sentences'
    }

    logger.info('Rendering sentences.html')

    return render(request, 'sentences.html', context)
