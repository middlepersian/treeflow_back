import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords


class Image(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    identifier = models.CharField(max_length=100)
    number = models.FloatField(null=True, blank=True)
    # In some cases, as in MK, images can have a source directly a "Codex" or a "Facsimile"
    source = models.ForeignKey('corpus.Source', on_delete=models.CASCADE, null=True,
                                  blank=True, related_name='image_source')
    previous = models.OneToOneField('self',
                                    related_name='next',
                                    blank=True,
                                    null=True,
                                    on_delete=models.DO_NOTHING)

    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['identifier', 'source', 'number'], name='identifier_source_number'
            )
        ]
        ordering = ['number']

    def __str__(self):
        return '{} - {}'.format(self.source, self.identifier)
