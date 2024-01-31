from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.cache import cache
from django.shortcuts import render
from django.db.models import Prefetch
import uuid
import logging
from treeflow.corpus.models import Text, Section, Token, SectionToken
from treeflow.datafeed.tasks import cache_all_texts  # Import the Celery task

logger = logging.getLogger(__name__)

@login_required
def sentences_view(request, text_id=None):
    logger.info('text_id : %s', text_id)

    # Fetching or caching texts
    cache_key_texts = "all_texts"
    texts = cache.get(cache_key_texts)
    if not texts:
        logger.info("Cache miss for texts - Fetching texts from database.")
        cache_all_texts.apply()  # Trigger the Celery task to update cache
        logger.info("Cache miss for texts - Triggered Celery task to update cache.")
        texts = cache.get(cache_key_texts)
        
    selected_text_id = text_id if text_id else request.GET.get('text_id')

    # Building the cache key for sentences
    cache_key_sentences = f"sentences_{selected_text_id}"
    sentences = cache.get(cache_key_sentences)

    if sentences is None:
        # Fetch and cache sentences if not cached
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
                    .only('id', 'image')
                )
            ) \
            .only('id', 'number', 'identifier')
        cache.set(cache_key_sentences, list(sentences), 300)
        logger.info("Cache miss for sentences")

    # Paginator setup
    paginator = Paginator(sentences, 10)

    # Fetching the correct page based on the page query parameter
    page_number = request.GET.get('page', 1)  # Default to first page or query parameter
    page_obj = paginator.get_page(page_number)
    logger.info("Page number: %s", page_number)

    context = {
        'texts': texts,
        'selected_text_id': selected_text_id or '',
        'page_obj': page_obj,
        'current_view': 'corpus:sentences'
    }

    return render(request, 'sentences.html', context)
