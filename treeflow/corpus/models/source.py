import uuid as uuid_lib
from django.db import models
from django.conf import settings
from .bibliography import BibEntry
from simple_history.models import HistoricalRecords


class Source(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    # codex, facsimile, edition, etc
    type = models.CharField(max_length=10, null=True, blank=True)

    identifier = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    references = models.ManyToManyField(BibEntry, blank=True)

    # a 'source' might have another sources as a source
    sources = models.ManyToManyField('self',blank=True, related_name='source_sources')
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()


    class Meta:
        ordering = ['identifier']
        constraints = [

            models.UniqueConstraint(
                fields=['type', 'identifier'], name='source_type_identifier'
            )
        ]
        indexes = [
            models.Index(fields=['type', 'identifier']),
        ]


    def __str__(self):
        return '{}'.format(self.identifier)