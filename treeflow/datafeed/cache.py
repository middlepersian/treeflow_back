from django.core.cache import cache
from django.db.models import Count
from treeflow.corpus.models import Text
from treeflow.corpus.utils.zotero import request_zotero_api_for_collection
import logging

logger = logging.getLogger(__name__)

def cache_all_zotero_sources():
    logger.debug("Running cache_all_zotero_sources task")

    group_key = "2116388"
    collection_key = "2CGA8RXR"

    zotero_data, _ = request_zotero_api_for_collection(group_key, collection_key)

    cache_key = 'zotero_sources'
    current_cache = cache.get(cache_key)

    if not current_cache:
        logger.info("Cache miss for sources - Sources have been updated in the cache.")
        cache.set(cache_key, zotero_data, timeout=3600)  # Set a 1-hour timeout
    else:
        logger.info("Cache hit for sources - Sources have not been updated in the cache.")
        cache.set(cache_key, current_cache, timeout=None)  # Set no timeout

def update_zotero_data_in_cache():
    logger.debug("Running update_zotero_data_in_cache task")

    collection_keys = {
    "Preliminary Publications": "4DBIWSQG",
    "Project Publications": "B3BHZEGW",
    "Related Publications": "8VFMBB74",
    "Presentations": "YZX3G3DF",
    "Related Presentations": "2DNQXANE",
    }

    publications = {
        'group_key': 2116388,
        'collections' : []
    }

    for key, value in collection_keys.items():
        zotero_data, _ = request_zotero_api_for_collection(publications["group_key"], value)
        publications["collections"].append({"name": key, "data": zotero_data})

    cache_key = 'zotero_publications'
    current_cache = cache.get(cache_key)

    if not current_cache:
        logger.info("Cache miss for publications - Publications have been updated in the cache.")
        cache.set(cache_key, publications['collections'], timeout=3600)  # Set a 1-hour timeout
    else:
        logger.info("Cache hit for publications - Publications have not been updated in the cache.")
        cache.set(cache_key, current_cache, timeout=None)  # Set no timeout


def cache_all_texts():
    logger.info("Running cache_all_texts task")
    cache_key_texts = "all_texts"
    current_cache = cache.get(cache_key_texts)

    if not current_cache:
        texts = Text.objects.annotate(token_count=Count('token_text')).order_by('identifier')
        cache.set(cache_key_texts, texts, 3600)  # Set a 1-hour timeout
        logger.info("Cache miss for texts - Texts have been updated in the cache.")
    else:
        logger.info("Cache hit for texts - Texts have not been updated in the cache.")
        cache.set(cache_key_texts, current_cache, timeout=None)
