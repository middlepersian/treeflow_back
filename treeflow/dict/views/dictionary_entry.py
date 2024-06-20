from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from treeflow.dict.models.lemma import Lemma
from treeflow.dict.models.sense import Sense
from treeflow.corpus.models.token import Token
from treeflow.corpus.models.section import Section

import logging

logger = logging.getLogger(__name__)


def lemma_details(request, lemma_id):
    lemma = Lemma.objects.prefetch_related('related_senses','related_senses__token_senses__section_tokens','related_senses__token_senses__lemmas').get(id=lemma_id)
    # tokens = [token for token in  lemma.first().token_lemmas.all()]
    # related_senses = [sense for sense in lemma.first().related_senses.all()]
    # lemma = lemma.first()
    context = {
        'lemma': lemma
    }
    
    return render(request, 'dictionary_entry.html', context)