from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django import forms
from django.views.generic.edit import FormView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator

from ..forms import SourceForm, BibEntryForm

from ..enums.deprel_enum import Deprel
from treeflow.corpus.models import BibEntry, Source

import logging

from treeflow.images.models import Image

# Set up logging
logger = logging.getLogger(__name__)


def manuscripts(request):
    """View function for home page of site."""

    # get all Sources of type manuscript
    manuscripts = Source.objects.filter(type="manuscript").order_by("identifier")

    # prefetch Images for each Source
    # for manuscript in manuscripts:
    #     manuscript.images = Image.objects.filter(source=manuscript)

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        "manuscripts.html",
        context={
            "manuscripts": manuscripts,
        },
    )


def get_images_for_manuscript(request,manuscript_id=None):
    # get the manuscript by its id
    manuscript = get_object_or_404(Source, id=manuscript_id)

    # get all images for the manuscript
    images = Image.objects.filter(source=manuscript).order_by("number")

    return render(
        request,
        "components/imageList.html",
        context={
            "manuscript":manuscript,
            "images":images,
        },
    )