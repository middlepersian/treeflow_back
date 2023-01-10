import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .folio import Folio


class Line(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    identifier = models.CharField(max_length=255, blank=True, null=True)
    folio = models.ForeignKey(Folio, on_delete=models.CASCADE, related_name='line_folio')
    number = models.FloatField(null=True, blank=True)
    number_in_text = models.FloatField(null=True, blank=True)
    previous = models.OneToOneField('self',
                                    related_name='next',
                                    blank=True,
                                    null=True,
                                    on_delete=models.DO_NOTHING)

    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['number', 'folio'], name='number_folio'
            )
        ]
        ordering = ['number']

    def __str__(self):
        return '{} - {}'.format(self.folio, self.number)
