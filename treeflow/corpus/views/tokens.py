from django.shortcuts import render
from django.core.paginator import Paginator
from treeflow.corpus.models import Text, Token, POS
from django.db.models import Prefetch


def tokens_view(request):
    # Get all Text objects for the dropdowns
    texts = Text.objects.all()
    # Get all pos choices
    pos_choices = POS.objects.order_by('pos').values_list('pos', flat=True).distinct()

    # Retrieve GET parameters
    selected_text_id = request.GET.get('text_id')

    # Start with an initial tokens queryset and prefetch related data
    tokens = Token.objects.prefetch_related(
        'lemmas',  # Prefetch related Lemma objects
        'senses',  # Prefetch related Senses objects
        'pos_token'  # Prefetch related POS objects
    )

    # Filter tokens if a text ID is provided
    if selected_text_id:
        tokens = tokens.filter(text__id=selected_text_id)

    # Setup paginator
    paginator = Paginator(tokens, 100)  # Show 100 tokens per page
    page_number = request.GET.get('page')
    tokens_page = paginator.get_page(page_number)

    # Prepare context for rendering
    context = {
        'texts': texts,
        'tokens': tokens_page,
        'pos_choices': pos_choices,
        'selected_text_id': selected_text_id or '',
    }

    # Render response
    return render(request, 'tokens.html', context)
