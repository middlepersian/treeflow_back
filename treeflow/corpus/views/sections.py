from django.shortcuts import render
from django.core.cache import cache
from django.db.models import Prefetch, prefetch_related_objects
from treeflow.corpus.models import Section, Token, Text, Source
from django.core import serializers
import logging
logger = logging.getLogger(__name__)

def sections_view(request, text_id=None):
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

    # Fetch or cache texts
    cache_key_texts = "all_texts"
    texts = cache.get(cache_key_texts)

    if not texts:
        logger.info("Cache miss for texts - Fetching texts from database.")
        texts = Text.objects.all()
        cache.set(cache_key_texts, texts)
        logger.info("Cache updated with texts from database.")

    selected_text_id = text_id or request.GET.get('text_id')
    logger.info('selected_text_id: %s', selected_text_id)

    cache_key = f"sections_for_text_{selected_text_id}"
    cached_data = cache.get(cache_key)

    token_queryset = Token.objects.only('transcription')
    prefetch = Prefetch('tokens', queryset=token_queryset, to_attr='prefetched_tokens')

    if cached_data:
        logger.info(f"Using cached sentences for text: {selected_text_id}")
        cached_sentence_ids = cached_data['sentence_ids']
        section_types = cached_data['section_types']

        sentence_sections = Section.objects.filter(
            id__in=cached_sentence_ids
        ).prefetch_related(prefetch)

    else:
        logger.info(f"Cache miss for sections of text: {selected_text_id}")
        all_sections = Section.objects.filter(text__id=selected_text_id)
        sentence_sections = all_sections.filter(type='sentence').prefetch_related(prefetch)
        section_types = list(all_sections.exclude(type='sentence').values_list('type', flat=True).distinct())

        cache.set(cache_key, {
            'sentence_ids': list(sentence_sections.values_list('id', flat=True)), 
            'section_types': section_types
        })

    context = {
        'texts': texts,
        'sentence_sections': sentence_sections,
        'section_types': section_types,
        'selected_text_id': selected_text_id or '',
        'current_view': 'corpus:sections',
        'manuscripts': manuscripts,  # Add manuscripts to the context
    }

    return render(request, 'sections.html', context)


