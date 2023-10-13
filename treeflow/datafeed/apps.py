import os
import logging

import celery

from django.apps import AppConfig

logger = logging.getLogger(__name__)
class DataFeedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'treeflow.datafeed'

    def ready(self):
        # Check if the current process is a Celery beat process
        if hasattr(celery, 'beat'):
            from .signals import start_warm_up_cache
            logger.info("Registering cache warming task.")
            start_warm_up_cache()
            logger.info("Cache warming task registered.")