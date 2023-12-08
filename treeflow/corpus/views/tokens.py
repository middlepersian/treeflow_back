from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Prefetch
from treeflow.corpus.models import Text, Token, POS, SectionToken
from treeflow.corpus.forms.feature_forms import FeatureFormSet

@login_required
def tokens_view(request, text_id=None):
    # Get all Text objects for the dropdowns
    texts = Text.objects.all()
    # Retrieve GET parameters
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
