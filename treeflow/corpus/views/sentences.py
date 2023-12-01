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
        # Set default text identifier if none is selected
    if not selected_text_id:
        logger.info("No text ID provided, using default text")
        default_text = Text.objects.filter(identifier="DMX-L19-01").first()
        if default_text:
            selected_text_id = default_text.id
            logger.info("Using default text ID: %s", selected_text_id)  

    # Prefetch objects for tokens with related POS, Features, and Lemmas
    token_prefetch = Prefetch(
        'tokens', 
        queryset=Token.objects.all().prefetch_related(
            'pos_token', 'feature_token', 'lemmas', 'senses'
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
    # log the number of tokens
    #logger.info("Found %s tokens", sentences.tokens.count())
    # how many tokens in the first sentence?
    logger.info("First sentence has %s tokens", sentences[0].tokens.count())

    # Prepare context for rendering
    context = {
        'texts': texts,
        'selected_text_id': selected_text_id or '',
        'page_obj': sentences_page,  # Include the page object for pagination controls
    }

    # Render response
    return render(request, 'sentences.html', context)
