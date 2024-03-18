import logging
from django.shortcuts import render, redirect, get_object_or_404
from treeflow.dict.forms.sense_form import SenseForm
from treeflow.dict.forms.lemma_form import LemmaForm
from treeflow.dict.models.lemma import Lemma

def lemma_edit(request, lemma_id):
    lemma_instance = None
    if lemma_id:
        lemma_instance = get_object_or_404(Lemma, id=lemma_id)

    lemma_form = LemmaForm(instance=lemma_instance)
    sense_form = SenseForm()

    context = {
        'lemma_form': lemma_form, 
        'sense_form': sense_form,
    }
    return render(request, 'lemma_form.html', context)