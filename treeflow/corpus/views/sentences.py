from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.core.cache import cache
from django.shortcuts import render
from django.db.models import Prefetch
from treeflow.corpus.models import Section, SectionToken, Token, Text
from treeflow.datafeed.tasks import cache_all_texts

import logging

logger = logging.getLogger(__name__)


@login_required
def sentences_view(request, text_id=None):
    logger.debug('Entering sentences_view with text_id: %s', text_id)

    # Fetching texts for the dropdown
    texts = cache.get_or_set("all_texts", lambda: Text.objects.all(), 300)
    logger.debug("Texts for dropdown: %d items", len(texts))

    selected_text_id = text_id if text_id else request.GET.get('text_id')
    logger.info('Selected text ID: %s', selected_text_id)

    if selected_text_id:
        # Prefetch for 'line' type sections related to tokens
        line_sections_prefetch = Prefetch(
            'sectiontoken_set',
            queryset=SectionToken.objects.filter(section__type='line').select_related('section'),
            to_attr='line_sections'
        )

        # Prefetch tokens with related data including line sections
        tokens_prefetch = Prefetch(
            'tokens',
            queryset=Token.objects.all()
            .select_related('image')
            .prefetch_related('lemmas', 'senses', 'pos_token', 'feature_token', 'comment_token', line_sections_prefetch)
        )

        # Building the cache key for sentences with tokens
        cache_key = f"sentences_with_tokens_{selected_text_id}"
        sentences = cache.get(cache_key)

        if sentences is None:
            logger.info("Cache miss - Fetching sentences and tokens from database.")
            sentences = Section.objects.filter(type='sentence', text=selected_text_id) \
                .prefetch_related(tokens_prefetch)
            cache.set(cache_key, list(sentences), 300)
            logger.debug("Fetched and cached %d sentences for text ID: %s", len(sentences), selected_text_id)
        else:
            logger.debug("Cache hit for text ID: %s", selected_text_id)

        paginator = Paginator(sentences, 10)  # Adjust the number per page as needed
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        logger.info("Page number: %s, Number of items on page: %d", page_number, len(page_obj))
    else:
        page_obj = Paginator(Section.objects.none(), 10).get_page(1)
        logger.info("No text ID selected, providing empty page object.")

    context = {
        'texts': texts,
        'selected_text_id': selected_text_id or '',
        'page_obj': page_obj,
        'current_view': 'corpus:sentences'
    }

    logger.info('Rendering sentences.html for text ID: %s', selected_text_id)
    return render(request, 'sentences.html', context)

