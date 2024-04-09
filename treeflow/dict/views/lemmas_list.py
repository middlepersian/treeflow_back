from django.shortcuts import render

from treeflow.dict.models.lemma import Lemma


def lemmas_list(request, lemma_id = None):
    lemmas = Lemma.objects.values('id', 'word')
    
    context = {
        'lemmas': lemmas,
    }

    if lemma_id:
        context['lemma_id'] = lemma_id
    
    return render(request, 'dictionary.html', context)