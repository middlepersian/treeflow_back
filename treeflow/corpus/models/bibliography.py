import uuid as uuid_lib
from django.db import models
from django.conf import settings

from simple_history.models import HistoricalRecords


class BibEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    # Zotero key
    key = models.CharField(blank=True, null=True, max_length=100, unique=True)

    history = HistoricalRecords()


    def __str__(self):
        return '{}'.format(self.key)
