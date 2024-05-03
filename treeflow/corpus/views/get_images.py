from django.http import JsonResponse
from treeflow.images.models import Image
from django.core.cache import cache

import logging

logger = logging.getLogger(__name__)


def get_images_view(request):
    source_identifier = request.GET.get("source_identifier", None)
 
    logger.info(f"source_identifier: {source_identifier}")

    cache_key_images = "images"
    images = cache.get(cache_key_images)

    if images is None:
        logger.info("Cache miss for images - Fetching images from database.")
        images = Image.objects.select_related("source")
        cache.set(cache_key_images, images)
    else:
        logger.info("Images already cached")

    if source_identifier:
        logger.info(f"Filtering images for source_identifier: {source_identifier}")
        images = images.filter(source__identifier=source_identifier)
        logger.info(f"Images: {images}")

    data = list(images.values())
    response = JsonResponse(data, safe=False)

    return response
