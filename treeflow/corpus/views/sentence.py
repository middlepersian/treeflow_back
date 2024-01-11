from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render

import logging
from treeflow.corpus.models import Section

logger = logging.getLogger(__name__)

@login_required
def sentence_view(request, sentence_id):
    try:
        sentence = Section.objects.get(id=sentence_id)
    except Section.DoesNotExist:
        logger.error("Invalid sentence_id or sentence not found in text")
        raise Http404("Sentence not found")

    context = {'sentence': sentence}

    return render(request, 'sentence.html', context)
