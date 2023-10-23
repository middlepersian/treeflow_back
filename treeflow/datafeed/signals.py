import logging
from celery import current_app
from .tasks import clear_and_warm_up_cache

logger = logging.getLogger(__name__)

already_started = False

def start_warm_up_cache(sender=None, **kwargs):
    global already_started
    if not already_started:
        logger.info("Starting cache warming task.")
        task = current_app.tasks.get('treeflow.datafeed.tasks.clear_and_warm_up_cache')
        task.apply_async()
        already_started = True
        logger.info("Cache warming task started.")
    else:
        logger.info("Cache warming task has already been started.")
