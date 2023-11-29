from django.shortcuts import render
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Prefetch
from treeflow.corpus.models import Text, Token, POS, SectionToken, Section, TokenLemma, TokenSense
from treeflow.dict.models import Lemma
import logging
from django.db.models import Prefetch
logger = logging.getLogger(__name__)


def sentences_view(request):
    # Get all Text objects for the dropdowns
    texts = Text.objects.all()
    # Retrieve GET parameters
    selected_text_id = request.GET.get('text_id')


    # Fetch sentences with optimized prefetch
    sentences = Section.objects.filter(type='sentence', text__id=selected_text_id)

        # Setup paginator
    paginator = Paginator(sentences, 20)  # Show 20 sentences per page
    page_number = request.GET.get('page')
    sentences_page = paginator.get_page(page_number)

    logger.debug(sentences.query)
    # print the numbers of sentences
    logger.debug(len(sentences))

    # Prepare context for rendering
    context = {
        'texts': texts,
        'sentences': sentences_page,
        'selected_text_id': selected_text_id or '',
    }

    return render(request, 'sentences.html', context)
