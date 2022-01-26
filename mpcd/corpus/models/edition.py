from django.db import models
from .author import Author
from .bibliography import BibEntry
from .text_sigle import TextSigle
from .source import Source
from simple_history.models import HistoricalRecords


class Edition(Source):
    authors = models.ManyToManyField(Author, blank=True, related_name='edition_authors')
    references = models.ManyToManyField(BibEntry, blank=True, related_name='edition_references')
    text_sigle = models.ManyToManyField(TextSigle, blank=True, related_name='edition_text_sigles')

    history = HistoricalRecords()
