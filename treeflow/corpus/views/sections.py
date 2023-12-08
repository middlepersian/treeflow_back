from django.shortcuts import render
from django.db.models import Prefetch
from treeflow.corpus.models import Section, Token, Text
from django.db.models import Count, Prefetch
from django.core import serializers
import logging
logger = logging.getLogger(__name__)


def sections_view(request, text_id=None):

    # Get all Text objects for the dropdowns
    texts = Text.objects.all()
    if text_id:
        selected_text_id = text_id
    else:
        selected_text_id = request.GET.get('text_id')

    # Define the queryset for tokens that prefetches the related section tokens for 'sentence' type sections
    token_queryset = Token.objects.filter(
        sectiontoken__section__text_id=text_id,
        sectiontoken__section__type='sentence'
    ).order_by('sectiontoken__section__number', 'number_in_sentence')

    # Create a Prefetch object for 'tokens' related to 'sentence' type sections
    tokens_prefetch = Prefetch(
        'tokens',
        queryset=token_queryset,
        to_attr='prefetched_tokens'
    )

    # Fetch all sections for the given text, applying the Prefetch object conditionally
    all_sections = Section.objects.filter(text__id=text_id).prefetch_related(
        'container'
    )

    sentence_sections = all_sections.filter(
        type='sentence').prefetch_related(tokens_prefetch)

    # log text id
    logger.info('selected_text_id id: %s', selected_text_id)

    # Get distinct section types
    section_types = Section.objects.order_by(
        'type').values_list('type', flat=True).distinct()
    # remove "sentence" from the types
    section_types = [x for x in section_types if x != 'sentence']
    # Pass the sentence_sections with prefetched tokens and other sections to the template
    context = {
        'texts': texts,
        'sentence_sections': sentence_sections,
        'section_types': section_types,
        'selected_text_id': selected_text_id or '',
        'current_view': 'corpus:sections',

    }

    return render(request, 'sections.html', context)
