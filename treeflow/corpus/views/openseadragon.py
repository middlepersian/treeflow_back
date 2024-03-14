
from django.shortcuts import render, get_object_or_404

import logging

from treeflow.images.models import Image
from treeflow.corpus.models import Source

# Set up logging
logger = logging.getLogger(__name__)


def openseadragon(request):
    """View function for home page of site."""
    # get the image by its id
    image_id = request.GET.get("image_id")
    logger.debug(f"image_id: {image_id}")
    if not image_id:
        return None
    image = Image.objects.get(id=image_id)
    logger.debug(f"image: {image}")
    return render(
        request,
        "components/OpenSeaDragon.html",
        context={
            "image": image.identifier,
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