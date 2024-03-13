from django.shortcuts import render
from django.core.cache import cache
from django.db.models import Prefetch, prefetch_related_objects
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

    cache_key = f"sections_for_text_{selected_text_id}"
    cached_data = cache.get(cache_key)

    # Adjust the prefetching relationship
    token_queryset = Token.objects.only('transcription')
    prefetch = Prefetch('tokens', queryset=token_queryset, to_attr='prefetched_tokens')

    if cached_data:
        cached_section_ids = cached_data['sentence_section_ids']
        section_types = cached_data['section_types']

        # Reconstruct the queryset using the cached IDs and apply prefetching
        sentence_sections = Section.objects.filter(
            id__in=cached_section_ids
        ).prefetch_related(prefetch)

        # Debugging: Check if prefetching is working correctly
        for section in sentence_sections:
            prefetched_tokens = getattr(section, 'prefetched_tokens', [])
            logger.debug(f"Section {section.id} has {len(prefetched_tokens)} tokens")

    else:
        logger.info(f"Cache miss for sections of text: {selected_text_id}")
        all_sections = Section.objects.filter(text__id=selected_text_id)
        sentence_sections = all_sections.filter(type='sentence').prefetch_related(prefetch)
        section_types = list(all_sections.exclude(type='sentence').values_list('type', flat=True).distinct())

        # Debugging: Check if prefetching is working correctly
        for section in sentence_sections:
            prefetched_tokens = getattr(section, 'prefetched_tokens', [])
            logger.debug(f"Section {section.id} has {len(prefetched_tokens)} tokens")

    context = {
        'texts': texts,
        'sentence_sections': sentence_sections,
        'section_types': section_types,
        'selected_text_id': selected_text_id or '',
        'current_view': 'corpus:sections',
    }

    return render(request, 'sections.html', context)
