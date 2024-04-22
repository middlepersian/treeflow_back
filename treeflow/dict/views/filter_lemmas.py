from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse

from treeflow.dict.models.lemma import Lemma
import re

import logging

logger = logging.getLogger(__name__)


def filter_lemmas(request):
    filter_word = request.GET.get('filter_word', '')
    search_mode = request.GET.get('search_mode', '')

    filter_modes = {
        'icontains': '__icontains',
        'iexact': '__iexact',
        'startswith': '__startswith',
        'endswith': '__endswith',
        'regex': '__regex',
    }

    # Default filter mode
    filter_mode = '__icontains' 

    if search_mode in filter_modes:
        filter_mode = filter_modes[search_mode]


    # Filter kwargs
    filter_kwargs = {}
    if filter_word:
        if search_mode == 'regex':
            logger.info(f"Regex search: {filter_word}")
            try:
                pattern = re.compile(filter_word)
                logger.info(f"Regex pattern: {pattern}")
                filter_kwargs[f'word{filter_mode}'] = pattern
            except re.error as e:
                logger.error(f"Regex compilation error: {e}")
                return HttpResponse(status=400)  
            
        filter_field = f'word{filter_mode}'
        filter_kwargs[filter_field] = filter_word

    # Filter query
    cached_query = cache.get('lemmas')
    if cached_query is not None and cached_query.exists():
        if filter_kwargs:
            filtered_lemmas = cached_query.filter(Q(**filter_kwargs))
        else:
            filtered_lemmas = cached_query.all()
    else:
        if filter_kwargs:
            filtered_lemmas = Lemma.objects.filter(Q(**filter_kwargs))
        else:
            filtered_lemmas = Lemma.objects.all()  

    # Div generation
    lemma_divs = []
    for lemma in filtered_lemmas:
        url = reverse('dict:lemma_details', kwargs={'lemma_id': lemma.id})

        div_html = (
            f'<div id="{lemma.id}" '
            f'hx-get="{url}" '
            f'hx-target="#lemma-details" '
            f'hx-replace-url="/dict/dictionary/{lemma.id}/" '
            f'onclick="selection(this)" '
            f'class="p-1 m-1 mb-0 text-center rounded-sm shadow-sm cursor-pointer '
            f'hover:text-white hover:bg-action shadow-black scroll-m-1">'
            f'{lemma.word}'
            f'</div>'
        )
        lemma_divs.append(div_html)

    lemma_html = '\n'.join(lemma_divs)

    return HttpResponse(lemma_html)
