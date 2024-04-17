from django.http import HttpResponse
from django.urls import resolve, reverse

from treeflow.dict.models.lemma import Lemma


def filter_lemmas(request):
    filter_word = request.GET.get('filter_word', '')

    # Perform filter query
    filtered_lemmas = Lemma.objects.filter(word__icontains=filter_word)

    # Generate HTML divs for filtered lemmas
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
