from django.shortcuts import render
from django.core.paginator import Paginator
from treeflow.corpus.models import Text, Token


def tokens_view(request):
    # Get all Text objects for the dropdowns
    texts = Text.objects.all()

    # Retrieve GET parameters
    selected_text_id = request.GET.get('text_id')

    # Start with an initial tokens queryset
    # and prefetch related data to minimize database hits
    tokens = Token.objects.prefetch_related(
        'lemmas',  # Prefetch related Lemma objects
        'senses',  # Prefetch related Senses objects
        'pos_token'  # Prefetch related Part-of-Speech objects
    )

    # Filter tokens if a text ID is provided
    if selected_text_id:
        tokens = tokens.filter(text__id=selected_text_id)

    # Setup paginator
    paginator = Paginator(tokens, 10)  # Show 10 tokens per page
    page_number = request.GET.get('page')
    tokens_page = paginator.get_page(page_number)

    # Prepare context for rendering
    context = {
        'texts': texts,
        'tokens': tokens_page,
        'selected_text_id': selected_text_id or '',
    }

    # Render response
    return render(request, 'tokens.html', context)
