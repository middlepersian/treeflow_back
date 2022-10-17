import uuid as uuid_lib
from typing import TYPE_CHECKING
from django.db import models
from simple_history.models import HistoricalRecords
from .facsimile import Facsimile

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager


class Folio(models.Model):

    line_folio: "RelatedManager[Line]"

    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    identifier = models.CharField(max_length=100)
    number = models.FloatField(null=True, blank=True)
    facsimile = models.ForeignKey(Facsimile, on_delete=models.CASCADE, null=True,
                                  blank=True, related_name='folio_facsimile')
    comments = models.ManyToManyField('Comment', blank=True, related_name='folio_comments')
    previous = models.OneToOneField('self',
                                    related_name='next',
                                    blank=True,
                                    null=True,
                                    on_delete=models.DO_NOTHING)

    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['identifier', 'facsimile', 'number'], name='identifier_facsimile_number'
            )
        ]
        ordering = ['number']

    def __str__(self):
        return '{} - {}'.format(self.facsimile, self.identifier)
