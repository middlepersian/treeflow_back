from django.shortcuts import render
from django.core.paginator import Paginator
from treeflow.corpus.models import Text, Section
import logging

logger = logging.getLogger(__name__)

def sentences_view(request):
    # Get all Text objects for the dropdowns
    texts = Text.objects.all()
    # Retrieve GET parameters
    selected_text_id = request.GET.get('text_id')
    page_number = int(request.GET.get('page', 1))

    # Define the number of sentences per page
    sentences_per_page = 10

    # Get the total count of sentences
    total_sentences_count = Section.objects.filter(type='sentence', text__id=selected_text_id).count()

    # Setup paginator with the total count
    paginator = Paginator(range(total_sentences_count), sentences_per_page)
    sentences_page = paginator.page(page_number)

    # Calculate the starting and ending points for the query
    start = (page_number - 1) * sentences_per_page
    end = start + sentences_per_page

    # Fetch only the sentences for the current page
    sentences = Section.objects.filter(type='sentence', text__id=selected_text_id).only('type', 'text', 'id', 'identifier').prefetch_related(
        'sectiontoken_set__token__lemmas',
        'sectiontoken_set__token__senses',
        'sectiontoken_set__token__pos_token'
    )[start:end]

    logger.debug(sentences.query)
    logger.debug(len(sentences))

    # Prepare context for rendering
    context = {
        'texts': texts,
        'sentences': sentences,
        'page_obj': sentences_page,
        'selected_text_id': selected_text_id or '',
    }

    return render(request, 'sentences.html', context)
