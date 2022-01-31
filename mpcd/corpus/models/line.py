import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .folio import Folio



class Line(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    number = models.IntegerField()
    folio = models.ForeignKey(Folio, on_delete=models.DO_NOTHING, related_name='line_folio')
    comment = models.TextField(blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.side, self.number)
