import uuid as uuid_lib
from django.db import models

from simple_history.models import HistoricalRecords


class Source(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, null=True)
    slug = models.SlugField(max_length=10, unique=True)
    description = models.CharField(max_length=255, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.slug)
