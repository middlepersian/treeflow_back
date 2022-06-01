import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords


class BibEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    # Zotero URL
    url = models.URLField(blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.url)
