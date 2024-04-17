from django.core.management.base import BaseCommand
from django.core.cache import cache
from treeflow.datafeed.cache import update_zotero_data_in_cache, cache_all_texts, cache_all_zotero_sources, cache_sections_for_texts, cache_manuscripts, cache_lemmas
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Manually clean cache and trigger tasks'

    def handle(self, *args, **kwargs):
        # Clean the cache
        cache.clear()
        logger.info("Cache has been cleared")
        # Call Huey tasks
        update_zotero_data_in_cache()
        cache_all_zotero_sources()
        cache_all_texts() 
        cache_sections_for_texts()
        cache_manuscripts()
        cache_lemmas()

        logger.info("Texts, Sections, Manuscripts, Lemmas and Zotero data have been updated in the cache")


