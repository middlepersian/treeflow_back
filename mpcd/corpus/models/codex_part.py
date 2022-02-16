import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from mpcd.corpus.models.codex import Codex


class CodexPart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    codex = models.ForeignKey(Codex, on_delete=models.CASCADE, related_name='codex_part_codex')
    # e.g "volume"
    part_type = models.CharField(max_length=50, blank=True, null=True)
    # e.g. "1"  or "1-2"
    part_number = models.CharField(max_length=10,
                                   blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.part_number)
