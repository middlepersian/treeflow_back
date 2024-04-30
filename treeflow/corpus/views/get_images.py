from django.http import JsonResponse
from treeflow.images.models import Image
from django.core.cache import cache

import logging

logger = logging.getLogger(__name__)


def get_images_view(request, source_id, manuscript_image=None):

    cache_key_images = f"images_{source_id}_{manuscript_image}"
    logger.info(f"source_id: {source_id}, manuscript_image: {manuscript_image}")
    images = cache.get(cache_key_images)
    
    logger.info(f"source_id: {source_id}, manuscript_image: {manuscript_image}")

    if images is None:
        logger.info("Cache miss for images - Fetching images from database.")
        images = Image.objects.select_related("source")

        cache.set(cache_key_images, images)
    else:
        logger.info("Images already cached")

    if manuscript_image:
        images = images.filter(identifier=manuscript_image)
        source = images.first().source
    else:
        images = images.filter(source_id=source_id)    

    data = list(images.values())
    response = JsonResponse(data, safe=False)

    # Add the manuscript_image and source to the response
    if manuscript_image:
        response['manuscript_image'] = manuscript_image
        response['source'] = source.identifier if source else source_id

    return response