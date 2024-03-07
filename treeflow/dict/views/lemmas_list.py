from django.shortcuts import render

from treeflow.dict.models.lemma import Lemma


def lemmas_list(request):
    lemmas = Lemma.objects.values('id', 'word')
    
    context = {
        'lemmas': lemmas,
    }
    
    return render(request, 'dictionary.html', context)