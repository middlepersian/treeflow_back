from django.core.cache import cache
from django.shortcuts import render

from treeflow.dict.models.lemma import Lemma

def lemmas_list(request, lemma_id = None):
    usesCache = False
    lemmas = cache.get('lemmas')

    if lemmas is None:
        print(f"({__name__}) Cache not available: Querying lemmas from database")
        lemmas = Lemma.objects.values('id', 'word')
    else:
        usesCache = True
        
    context = {
        'lemmas': lemmas,
    }

    if lemma_id:
        context['lemma_id'] = lemma_id
        lemma = lemmas.filter(id=lemma_id).first()
        context['lemma_first_letter'] = lemma['word'][0].lower() if not usesCache else lemma.word[0].lower()
    return render(request, 'dictionary.html', context)