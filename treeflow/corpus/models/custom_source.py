from django.db import models
from .bibliography import BibEntry
from .source import Source
from simple_history.models import HistoricalRecords
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomSource(Source):
    authors = models.ManyToManyField(User, blank=True, related_name='custom_source_authors')
    references = models.ManyToManyField(BibEntry, blank=True, related_name='custom_source_references')

    history = HistoricalRecords()
