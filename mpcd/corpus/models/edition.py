import uuid as uuid_lib
from django.db import models
from .author import Author
from .bibliography import BibEntry
from simple_history.models import HistoricalRecords


class Edition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=255)
    author = models.ManyToManyField(Author, blank=True)
    references = models.ManyToManyField(BibEntry, blank=True)

    description = models.TextField(blank=True)
    history = HistoricalRecords()
