
from django.shortcuts import render, get_object_or_404

import logging

from treeflow.images.models import Image
from treeflow.corpus.models import Source

# Set up logging
logger = logging.getLogger(__name__)


def openseadragon(request):
    sources = Source.objects.filter(type="manuscript").order_by("identifier")
    return render (
        request,
        "components/OpenSeaDragon.html",
        context={
            "sources": sources,
        },
    )

def sourceSelector(request):
    sources = Source.objects.filter(type="manuscript").order_by("identifier")
    return render (
        request,
        "components/sourceSelector.html",
        context={
            "sources": sources,
        },
    )

def imageSelector(request):
    source_id = request.GET.get("source_id")
    logger.debug(f"source_id: {source_id}")
    if not source_id:
        return render (
            request,
            "components/imageSelector.html",
            context={
                "source": None,
                "images": None,
            },
        )
    source = get_object_or_404(Source, id=source_id)
    images = Image.objects.filter(source=source).order_by("number")
    return render (
        request,
        "components/imageSelector.html",
        context={
            "source": source,
            "images": images,
        },
    )