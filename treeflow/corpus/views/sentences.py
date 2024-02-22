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

import logging

logger = logging.getLogger(__name__)

@login_required
def sentences_view(request, text_id=None):
    logger.info("Accessed sentences_view with text_id: %s", text_id)

    texts = cache.get_or_set("all_texts", lambda: Text.objects.all())
    logger.debug("Fetched texts for dropdown, total count: %d", len(texts))

    selected_text_id = text_id if text_id else request.GET.get('text_id')
    logger.info("Selected text ID for fetching sentences: %s", selected_text_id)

    if selected_text_id:
        cache_key = f"sentences_{selected_text_id}"
        sentences = cache.get(cache_key)

        if sentences is None:
            logger.info("Cache miss - Fetching sentences from database for text ID: %s", selected_text_id)
            sentences = Section.objects.filter(type='sentence', text=selected_text_id).prefetch_related('senses')
            cache.set(cache_key, list(sentences), 300)
            logger.debug("Cached %d sentences for text ID: %s", len(sentences), selected_text_id)
        else:
            logger.debug("Cache hit - Retrieved sentences from cache for text ID: %s", selected_text_id)

        paginator = Paginator(sentences, 10)  # Adjust the number per page as needed
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        logger.info("Paginated sentences, page number: %s, total items on page: %d", page_number, len(page_obj))

        # Load tokens for sentences on the current page
        for sentence in page_obj:
            section_tokens = SectionToken.objects.filter(section=sentence)
            token_ids = section_tokens.values_list('token', flat=True)
            tokens = Token.objects.filter(id__in=token_ids).select_related('image').prefetch_related('lemmas', 'senses', 'pos_token', 'feature_token', 'comment_token')
            setattr(sentence, 'tokens_list', tokens)
            logger.debug("Loaded tokens for sentence ID: %s, total tokens: %d", sentence.id, len(tokens))

    else:
        page_obj = Paginator(Section.objects.none(), 10).get_page(1)
        logger.info("No text ID selected, providing empty paginator.")

    context = {
        'texts': texts,
        'selected_text_id': selected_text_id or '',
        'page_obj': page_obj,
        'current_view': 'corpus:sentences'
    }

    logger.info("Rendering sentences.html for text ID: %s", selected_text_id)
    return render(request, 'sentences.html', context)
