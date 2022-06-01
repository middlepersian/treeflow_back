import uuid as uuid_lib
from django.db import models
from .bibliography import BibEntry
from simple_history.models import HistoricalRecords


class Source(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)

    slug = models.SlugField(max_length=10, unique=True)
    bib_entry = models.ForeignKey(BibEntry, on_delete=models.DO_NOTHING, null=True,
                                  blank=True, related_name='source_bib_entry')
    description = models.TextField(null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.slug)
