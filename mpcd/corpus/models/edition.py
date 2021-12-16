import uuid as uuid_lib
from django.db import models
from .author import Author
from .bibliography import BibEntry
from .sigle import TextSigle
from simple_history.models import HistoricalRecords


class Edition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, blank=True)
    references = models.ManyToManyField(BibEntry, blank=True)
    text_sigle = models.ForeignKey(TextSigle, on_delete=models.CASCADE, null=True)

    description = models.TextField(blank=True)
    history = HistoricalRecords()
