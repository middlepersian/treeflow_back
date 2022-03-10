import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .facsimile import Facsimile


class Folio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    identifier = models.CharField(max_length=100)
    number = models.FloatField(null=True, blank=True)
    facsimile = models.ForeignKey(Facsimile, on_delete=models.CASCADE, null=True,
                                  blank=True, related_name='folio_facsimile')
    comment = models.CharField(max_length=255, blank=True)
    previous = models.OneToOneField('self',
                                    related_name='next',
                                    blank=True,
                                    null=True,
                                    on_delete=models.DO_NOTHING)

    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['identifier', 'facsimile'], name='identifier_facsimile'
            )
        ]
        ordering = ['number']

    def __str__(self):
        return '{}'.format(self.identifier)
