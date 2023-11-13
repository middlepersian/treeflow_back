from django.shortcuts import render
from django.db.models import Prefetch
from treeflow.corpus.models import Section, Token

from django.db.models import Prefetch

def text_sections_view(request, text_id):
    # Define the queryset for tokens that prefetches the related section tokens
    # Filter the tokens through the 'SectionToken' intermediary table
    token_queryset = Token.objects.filter(
        sectiontoken__section__text_id=text_id,
        sectiontoken__section__type='sentence'
    ).order_by('sectiontoken__section__number', 'number_in_sentence')

    # Create a Prefetch object specifically for 'section_tokens' related to 'sentence' type sections
    # The 'to_attr' parameter specifies the attribute name where the prefetched tokens will be stored
    tokens_prefetch = Prefetch(
        'tokens', 
        queryset=token_queryset,
        to_attr='prefetched_tokens'
    )

    # Fetch sections of type 'sentence' for the given text, using the Prefetch object
    sections = Section.objects.filter(
        text__id=text_id, 
        type='sentence'
    ).prefetch_related(tokens_prefetch)
    # Pass the sentence_sections with prefetched tokens to the template
    context = {
        'sections': sections,
    }

    return render(request, 'text_sections.html', context)
