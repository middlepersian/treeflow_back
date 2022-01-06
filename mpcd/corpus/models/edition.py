from django.db import models
from .author import Author
from .bibliography import BibEntry
from .sigle import TextSigle
from .source import Source
from simple_history.models import HistoricalRecords


class Edition(Source):
    authors = models.ManyToManyField(Author, blank=True)
    references = models.ManyToManyField(BibEntry, blank=True)
    text_sigle = models.ManyToManyField(TextSigle, blank=True)

    history = HistoricalRecords()

