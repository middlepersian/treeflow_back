from django.core.management.base import BaseCommand
from django.core.cache import cache
from treeflow.datafeed.cache import update_zotero_data_in_cache, cache_all_texts, cache_all_zotero_sources
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Manually clean cache and trigger tasks'

    def handle(self, *args, **kwargs):
        # Clean the cache
        cache.clear()
        logger.debug("Cache has been cleared")
        # Call Huey tasks
        update_zotero_data_in_cache()
        cache_all_zotero_sources()
        cache_all_texts() 
        logger.debug("Text and Zotero data have been updated in the cache")


