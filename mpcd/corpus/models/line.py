import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from ordered_model.models import OrderedModel
from .folio import Folio


class Line(OrderedModel):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    number = models.PositiveSmallIntegerField()
    folio = models.ForeignKey(Folio, on_delete=models.CASCADE, related_name='line_folio')
    comment = models.TextField(blank=True)
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
        #order_with_respect_to = 'previous'

    def __str__(self):
        return '{}'.format(self.number)
