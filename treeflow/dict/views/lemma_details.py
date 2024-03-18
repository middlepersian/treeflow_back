from django.shortcuts import render, get_object_or_404
from treeflow.dict.models.lemma import Lemma


def lemma_details(request, lemma_id):
    lemma = get_object_or_404(Lemma, id=lemma_id)
    related_lemmas = lemma.related_lemmas.all()
    related_senses = lemma.related_senses.all()

    context = {
        'id': lemma.id,
        'word': lemma.word,
        'language': lemma.language,
        'categories': lemma.categories,
        'multiword_expression': lemma.multiword_expression,
        'related_lemmas': related_lemmas,
        'related_senses': related_senses,
    }
    
    return render(request, 'lemma_details.html', context)