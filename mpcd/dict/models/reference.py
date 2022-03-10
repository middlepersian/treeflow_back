import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords


class Reference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    reference = models.CharField(unique=True, max_length=350, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['reference']

    def __str__(self):
        return '{}'.format(self.reference)
