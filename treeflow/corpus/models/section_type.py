from django.db import models
import uuid as uuid_lib
from simple_history.models import HistoricalRecords


class SectionType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    identifier = models.CharField(max_length=30, unique=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.identifier)
