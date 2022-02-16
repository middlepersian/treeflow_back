import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from mpcd.corpus.models.bibliography import BibEntry
from mpcd.corpus.models.codex_part import CodexPart


class Facsimile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    reference = models.ForeignKey(BibEntry, on_delete=models.CASCADE, related_name='facsimile_reference')
    codex_part = models.ForeignKey(CodexPart, on_delete=models.CASCADE, null=True,
                                   blank=True, related_name='facsimile_codex_part')
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.slug)
