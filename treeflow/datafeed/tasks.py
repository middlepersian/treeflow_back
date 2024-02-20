from huey.contrib.djhuey import task, periodic_task, db_task, db_periodic_task, enqueue
from huey import crontab
from huey import RedisHuey
from django.core.cache import cache
from treeflow.corpus.models import Text
from treeflow.corpus.utils.zotero import request_zotero_api_for_collection
from treeflow.datafeed.cache import update_zotero_data_in_cache, cache_all_texts, cache_all_zotero_sources, cache_sections_for_texts
import logging

logger = logging.getLogger(__name__)

@periodic_task(crontab(hour='*', minute=0))
def periodic_update_zotero_data_in_cache():
    logger.info("Running periodic_update_zotero_data_in_cache task")
    update_zotero_data_in_cache()

@periodic_task(crontab(hour='*', minute=0))
def periodic_cache_all_zotero_sources():
    logger.info("Running periodic_cache_all_zotero_sources task")
    cache_all_zotero_sources()

@db_periodic_task(crontab(hour='*', minute=0))
def periodic_cache_all_texts_and_sections():
    logger.info("Running combined periodic_cache tasks")
    cache_texts_task = cache_all_texts.s()
    cache_sections_task = cache_sections_for_texts.s()

    # Chain the tasks
    pipeline = cache_texts_task.then(cache_sections_task)
    enqueue(pipeline)
