import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .codex import Codex




class Folio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    identifier = models.CharField(max_length=100)
    codex = models.ForeignKey(Codex, on_delete=models.CASCADE, related_name='folio_codex')
    comment = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.name)

