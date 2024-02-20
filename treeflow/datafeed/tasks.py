from huey.contrib.djhuey import task, periodic_task, db_task, db_periodic_task, enqueue
from huey import crontab
from huey import RedisHuey
from django.core.cache import cache
from treeflow.corpus.models import Text
from treeflow.corpus.utils.zotero import request_zotero_api_for_collection
from treeflow.datafeed.cache import update_zotero_data_in_cache, cache_all_texts, cache_all_zotero_sources, cache_sections_for_texts
import logging

logger = logging.getLogger(__name__)

@task()
def update_zotero_data_in_cache_task():
    logger.info("Running periodic_update_zotero_data_in_cache task")
    update_zotero_data_in_cache()

@task()
def cache_all_zotero_sources_task():
    logger.info("Running periodic_cache_all_zotero_sources task")
    cache_all_zotero_sources()

@task()
def cache_all_texts_task():
    cache_all_texts()

@task()
def cache_sections_for_texts_task():
    cache_sections_for_texts()

@task()
def clear_cache_task():
    logger.info("Clearing cache")
    cache.clear()

@db_periodic_task(crontab(hour='*', minute=0))
def periodic_cache_all_texts_and_sections_task():
    logger.info("Running combined periodic_cache tasks")
    clear_cache = clear_cache_task.s()
    cache_texts = cache_all_texts_task.s()
    cache_sections = cache_sections_for_texts_task.s()

    # Chain the tasks: clear cache -> cache all texts -> cache sections
    pipeline = clear_cache.then(cache_texts).then(cache_sections)
    enqueue(pipeline)

@db_periodic_task(crontab(hour='*', minute=0))
def periodic_zotero_tasks_task():
    logger.info("Running combined Zotero periodic tasks")
    update_zotero_data = update_zotero_data_in_cache_task.s()
    cache_zotero_sources = cache_all_zotero_sources_task.s()

    # Chain the Zotero tasks
    zotero_pipeline = update_zotero_data.then(cache_zotero_sources)
    enqueue(zotero_pipeline)
