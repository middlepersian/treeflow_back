from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Prefetch
from treeflow.corpus.models import Text, Token, POS, SectionToken
from treeflow.corpus.forms.feature_forms import FeatureFormSet
from treeflow.datafeed.tasks import cache_all_texts  # Import the Celery task


import logging
logger = logging.getLogger(__name__)

@login_required
def tokens_view(request, text_id=None):
    cache_key_texts = "all_texts"
    texts = cache.get(cache_key_texts)

    if not texts:
        logger.info("Cache miss for texts - Fetching texts from database.")
        cache_all_texts.apply()  # Trigger the Celery task to update cache
        logger.info("Cache miss for texts - Triggered Celery task to update cache.")
        texts = cache.get(cache_key_texts)

    selected_text_id = text_id

    # Prefetch for sections of type 'sentence'
    sentence_prefetch = Prefetch(
        'sectiontoken_set',
        queryset=SectionToken.objects.filter(
            section__type='sentence').select_related('section'),
        to_attr='sentence_sections'
    )

    # Prefetch for sections of type 'line'
    line_prefetch = Prefetch(
        'sectiontoken_set',
        queryset=SectionToken.objects.filter(
            section__type='line').select_related('section'),
        to_attr='line_sections'
    )

    # Start with an initial tokens queryset and prefetch related data
    tokens = Token.objects.prefetch_related(
        'lemmas',  # Prefetch related Lemma objects
        'senses',  # Prefetch related Senses objects
        'pos_token',  # Prefetch related POS objects
        'feature_token',  # Prefetch related Feature objects,
        'comment_token',  # Prefetch related Comment objects,
        sentence_prefetch,  # Prefetch related Sentence sections
        line_prefetch,  # Prefetch related Line sections
    )


    # Filter tokens if a text ID is provided
    if selected_text_id:
        tokens = tokens.filter(text__id=selected_text_id)

    # Setup paginator
    paginator = Paginator(tokens, 150)  # Show 100 tokens per page
    page_number = request.GET.get('page')
    tokens_page = paginator.get_page(page_number)

    # Prepare context for rendering
    context = {
        'texts': texts,
        'tokens': tokens_page,
        'selected_text_id': selected_text_id or '',
        'current_view': 'corpus:tokens',
    }

    # Render response
    return render(request, 'tokens.html', context)
