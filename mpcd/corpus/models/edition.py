from django.db import models
from .bibliography import BibEntry
from .text_sigle import TextSigle
from .source import Source
from simple_history.models import HistoricalRecords


class Edition(Source):
    references = models.ManyToManyField(BibEntry, blank=True, related_name='edition_references')
    text_sigles = models.ManyToManyField(TextSigle, blank=True, related_name='edition_text_sigles')

    history = HistoricalRecords()
