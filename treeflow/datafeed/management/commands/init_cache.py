from django.core.management.base import BaseCommand
from treeflow.tasks import update_zotero_data_in_cache, cache_all_texts
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Initializes the cache'

    def handle(self, *args, **kwargs):
        logger.info('Initializing cache with Zotero data')
        update_zotero_data_in_cache.apply()
        logger.info('Initializing cache with texts')
        cache_all_texts.apply()
