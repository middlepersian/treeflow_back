from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords



class CustomSource(Source):
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='custom_source_authors')
    references = models.ManyToManyField(BibEntry, blank=True, related_name='custom_source_references')
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()
