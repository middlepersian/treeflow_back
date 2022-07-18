import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .folio import Folio


class Line(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    number = models.FloatField(null=True, blank=True)
    folio = models.ForeignKey(Folio, on_delete=models.CASCADE, related_name='line_folio')
    comments = models.ManyToManyField('Comment', blank=True, related_name = 'line_comments')
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
        return '{}'.format(self.number)
