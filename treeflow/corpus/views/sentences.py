from treeflow.corpus.models import Text, Section, Token, SectionToken
from django.core.paginator import Paginator, EmptyPage
from django.core.cache import cache
from django.shortcuts import render
from django.db.models import Prefetch
import logging

logger = logging.getLogger(__name__)

def sentences_view(request):
    # Get all Text objects for the dropdowns
    texts = Text.objects.all()
    # Retrieve GET parameters
    selected_text_id = request.GET.get('text_id')


    # Retrieve all sentences (sections of type 'sentence')
    sentences = Section.objects.filter(type='sentence')
    # Prefetch for sections of type 'sentence'
    sentence_prefetch = Prefetch(
        'sectiontoken_set',
        queryset=SectionToken.objects.filter(section__type='sentence').select_related('section'),
        to_attr='sentence_sections'
    )

    # Prefetch for sections of type 'line'
    line_prefetch = Prefetch(
        'sectiontoken_set',
        queryset=SectionToken.objects.filter(section__type='line').select_related('section'),
        to_attr='line_sections'
    )
    # If a text ID is provided, filter sentences by this text
    if selected_text_id:
        sentences = sentences.filter(text__id=selected_text_id)

    # Setup paginator for sentences
    paginator = Paginator(sentences, 10)  # Adjust the number of sentences per page as needed
    page_number = request.GET.get('page')
    sentences_page = paginator.get_page(page_number)

    # Retrieve tokens for each sentence in the current page
    tokens_by_sentence = []
    for sentence in sentences_page:
        tokens = Token.objects.filter(
            sectiontoken__section=sentence
        ).prefetch_related(
            'lemmas', 'senses', 'pos_token', 'feature_token',  # Prefetch related objects
            sentence_prefetch, line_prefetch
        )
        tokens_by_sentence.append((sentence, tokens))

    # Prepare context for rendering
    context = {
        'texts': texts,
        'sentences_with_tokens': tokens_by_sentence,
        'selected_text_id': selected_text_id or '',
        'page_obj': sentences_page,  # Include the page object for pagination controls
    }

        # Render response
    return render(request, 'sentences.html', context)
