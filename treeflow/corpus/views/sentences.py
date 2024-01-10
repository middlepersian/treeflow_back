from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.cache import cache
from django.shortcuts import render
from django.db.models import Prefetch
import uuid
import logging
from treeflow.corpus.models import Text, Section, Token, SectionToken

logger = logging.getLogger(__name__)


@login_required
def sentences_view(request, text_id=None, sentence_id=None):
    logger.info('text_id : %s', text_id)

    # Cache key base for sentences and texts
    cache_base_key_sentences = f"sentences_page_{text_id}_"
    cache_key_texts = "all_texts"

    # Check cache for texts
    texts = cache.get(cache_key_texts)
    if not texts:
        texts = Text.objects.all()
        cache.set(cache_key_texts, texts, 300)  # Cache for 5 minutes
        logger.info("Cache miss for texts")

    selected_text_id = text_id if text_id else request.GET.get('text_id')

    line_prefetch = Prefetch(
        'sectiontoken_set',
        queryset=SectionToken.objects.filter(
            section__type='line').select_related('section'),
        to_attr='line_sections'
    )

    # Prefetch for tokens with necessary related objects
    tokens_prefetch = Prefetch(
        'tokens',
        queryset=Token.objects.select_related('image')
        .prefetch_related('pos_token', 'feature_token', 'lemmas', 'senses', 'comment_token', line_prefetch)
        .only('id', 'image')  # Adjust fields as per your requirement
    )

    # Sentence query with optimized prefetching
    sentences = Section.objects.filter(type='sentence', text=selected_text_id) \
        .prefetch_related(tokens_prefetch) \
        .only('id', 'number', 'identifier', 'title', 'language')  # Only fetch necessary fields

    # Setup paginator for sentences
    paginator = Paginator(sentences, 10)

    # Check if sentence_id is provided
    if sentence_id:
        # Calculate page_number based on sentence_id
        try:
            sentence_number = sentences.get(id=sentence_id).number
            sentence_index = sentences.filter(number__lte=sentence_number).count()
            page_number = (sentence_index - 1) // paginator.per_page + 1
        except Section.DoesNotExist:
            page_number = 1
    else:
        page_number = request.GET.get('page', 1)

    # Generate cache key for sentences
    cache_key_sentences = f"{cache_base_key_sentences}{page_number}"

    # Check cache for sentences page
    sentences_page = cache.get(cache_key_sentences)
    if not sentences_page:
        sentences_page = paginator.get_page(page_number)
        cache.set(cache_key_sentences, sentences_page, 300)  # Cache for 5 minutes
        logger.info("Cache miss for sentences")

    logger.info("Found %s sentences", sentences.count())

    # Pass 'prepared_data' to the template
    context = {
        'texts': texts,
        'selected_text_id': selected_text_id or '',
        'page_obj': sentences_page,
        'current_view': 'corpus:sentences',
    }

    return render(request, 'sentences.html', context)
