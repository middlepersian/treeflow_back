from django.shortcuts import render
from django.db.models import Prefetch
from treeflow.corpus.models import Section, Token
from django.db.models import Count, Prefetch
from django.core import serializers

from collections import defaultdict


def sections_editor_view(request, text_id):
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

    sentence_sections = all_sections.filter(type='sentence').prefetch_related(tokens_prefetch)

    # Get distinct section types
    section_types = Section.objects.order_by('type').values_list('type', flat=True).distinct()
    #remove "sentence" from the types
    section_types = [x for x in section_types if x != 'sentence']
    # Pass the sentence_sections with prefetched tokens and other sections to the template
    context = {
        'sentence_sections': sentence_sections,
        'section_types': section_types,
        'all_sections': all_sections,
    }

    return render(request, 'sections_editor.html', context)
