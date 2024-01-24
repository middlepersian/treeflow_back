from huey.contrib.djhuey import task, periodic_task, db_task, db_periodic_task
from huey import crontab
from huey import RedisHuey
from django.core.cache import cache
from treeflow.corpus.models import Text
from treeflow.corpus.utils.zotero import request_zotero_api_for_collection
from treeflow.datafeed.cache import update_zotero_data_in_cache, cache_all_texts
import logging

logger = logging.getLogger(__name__)

@periodic_task(crontab(hour='*', minute=0))
def periodic_update_zotero_data_in_cache():
    logger.info("Running periodic_update_zotero_data_in_cache task")
    update_zotero_data_in_cache()

@db_periodic_task(crontab(hour='*', minute=0))
def periodic_cache_all_texts():
    logger.info("Running periodic_cache_all_texts task")
    cache_all_texts()
        
@db_periodic_task(crontab(minute='*/1'))
def every_min():
    logger.info("Running every min task")
    pass