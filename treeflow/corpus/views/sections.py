from django.shortcuts import render
from django.core.cache import cache
from django.db.models import Prefetch
from treeflow.corpus.models import Section, Token, Text
from treeflow.datafeed.tasks import cache_all_texts  # Import the Celery task
from django.core import serializers
import logging
logger = logging.getLogger(__name__)


def sections_view(request, text_id=None):
    cache_key_texts = "all_texts"
    texts = cache.get(cache_key_texts)

    if not texts:
        logger.info("Cache miss for texts - Fetching texts from database.")
        cache_all_texts.apply()  
        logger.info("Cache miss for texts - Triggered Huey task to update cache.")
        texts = cache.get(cache_key_texts)
        
    if text_id:
        selected_text_id = text_id
    else:
        selected_text_id = request.GET.get('text_id')

    # Define the queryset for tokens
    token_queryset = Token.objects.filter(
        sectiontoken__section__text_id=selected_text_id,
        sectiontoken__section__type='sentence'
    ).order_by('sectiontoken__section__number', 'number_in_sentence')

    # Create a Prefetch object for tokens
    tokens_prefetch = Prefetch(
        'tokens',
        queryset=token_queryset,
        to_attr='prefetched_tokens'
    )

    # Fetch all sections for the given text
    all_sections = Section.objects.filter(text__id=selected_text_id).prefetch_related(
        'container'
    )

    sentence_sections = all_sections.filter(
        type='sentence').prefetch_related(tokens_prefetch)

    logger.info('selected_text_id id: %s', selected_text_id)

    # Get distinct section types
    section_types = Section.objects.order_by(
        'type').values_list('type', flat=True).distinct()
    section_types = [x for x in section_types if x != 'sentence']

    context = {
        'texts': texts,
        'sentence_sections': sentence_sections,
        'section_types': section_types,
        'selected_text_id': selected_text_id or '',
        'current_view': 'corpus:sections',
    }

    return render(request, 'sections.html', context)