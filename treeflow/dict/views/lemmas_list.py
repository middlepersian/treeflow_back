from django.core.cache import cache
from django.shortcuts import render

from treeflow.dict.models.lemma import Lemma

def lemmas_list(request, lemma_id = None):
    lemmas = cache.get('lemmas')

    if lemmas is None:
        lemmas = Lemma.objects.values('id', 'word')
        
    context = {
        'lemmas': lemmas,
    }

    if lemma_id:
        context['lemma_id'] = lemma_id
    
    return render(request, 'dictionary.html', context)