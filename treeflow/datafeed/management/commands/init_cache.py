from django.core.management.base import BaseCommand
from django.core.cache import cache
from treeflow.datafeed.cache import update_zotero_data_in_cache, cache_all_texts, cache_all_zotero_sources, cache_sections_for_texts
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
        cache_sections_for_texts()
        logger.debug("Texts, Sections and Zotero data have been updated in the cache")


