import uuid as uuid_lib
from django.db import models
from .bibliography import BibEntry
from simple_history.models import HistoricalRecords


class Source(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    # codex, facsimile, edition, etc
    type = models.CharField(max_length=10, null=True, blank=True)

    identifier = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    references = models.ManyToManyField(BibEntry, related_name='source_references')

    # a 'source' might have another sources as a source
    sources = models.ManyToManyField('self', related_name='source_sources', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()


    def __str__(self):
        return '{}'.format(self.identifier)