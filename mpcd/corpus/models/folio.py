import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .codex import Codex


class Folio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    codex = models.ForeignKey(Codex, on_delete=models.CASCADE, related_name='folio_codex')
    position_in_codex = models.PositiveSmallIntegerField(default=0)
    identifier = models.CharField(max_length=100)
    comment = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords()
    previous = models.OneToOneField('self',
                                    related_name='next',
                                    blank=True,
                                    null=True,
                                    on_delete=models.DO_NOTHING)
  

    def __str__(self):
        return '{}'.format(self.name)
