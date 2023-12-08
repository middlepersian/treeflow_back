from treeflow.corpus.models import Text, Section, Token, SectionToken
from django.core.paginator import Paginator, EmptyPage
from django.core.cache import cache
from django.shortcuts import render
from django.db.models import Prefetch
import logging

logger = logging.getLogger(__name__)


def sentences_view(request, text_id=None):
    # Get all Text objects for the dropdowns
    texts = Text.objects.all()
    if text_id:
        selected_text_id = text_id
    else: 
        selected_text_id = request.GET.get('text_id')


    # Prefetch for sections of type 'line'
    line_prefetch = Prefetch(
        'sectiontoken_set',
        queryset=SectionToken.objects.filter(section__type='line').select_related('section'),
        to_attr='line_sections'
    )

    # Prefetch objects for tokens with related POS, Features, and Lemmas
    token_prefetch = Prefetch(
        'tokens',
        queryset=Token.objects.all().select_related('image').prefetch_related(
            'pos_token', 'feature_token', 'lemmas', 'senses', line_prefetch
        )
    )

    # Query for sentences with selected text ID and prefetch related tokens
    sentences = Section.objects.filter(
        type='sentence', text=selected_text_id
    ).prefetch_related(token_prefetch)

    # Setup paginator for sentences
    paginator = Paginator(sentences, 10)  # Adjust the number of sentences per page as needed
    page_number = request.GET.get('page')
    sentences_page = paginator.get_page(page_number)

    # log the number of sentences
    logger.info("Found %s sentences", sentences.count())


    # Prepare context for rendering
    context = {
        'texts': texts,
        'selected_text_id': selected_text_id or '',
        'page_obj': sentences_page,  
        'current_view': 'corpus:sentences',
    }

    # Render response
    return render(request, 'sentences.html', context)
