from django.shortcuts import render
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Prefetch
from treeflow.corpus.models import Text, Token, POS, SectionToken, Section
import logging
logger = logging.getLogger(__name__)

def sentences_view(request):
    # Get all Text objects for the dropdowns
    texts = Text.objects.all()
    # Retrieve GET parameters
    selected_text_id = request.GET.get('text_id')

    # Fetch sentences with their tokens for the selected text
    sentences = Section.objects.filter(type='sentence', text_id=selected_text_id).prefetch_related(
        Prefetch(
            'sectiontoken_set',
            queryset=SectionToken.objects.filter(token__text_id=selected_text_id).select_related('token').prefetch_related(
                'token__lemmas', 'token__senses', 'token__pos_token', 'token__feature_token'
            ),
            to_attr='tokens'
        )
    )
    logger.debug(sentences.query)
    # print the numbers of sentences
    logger.debug(len(sentences))

    # Prepare context for rendering
    context = {
        'texts': texts,
        'sentences': sentences,
        'selected_text_id': selected_text_id or '',
    }

    return render(request, 'sentences.html', context)
