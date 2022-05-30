import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .language import LanguageChoices


class Definition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    definition = models.TextField(unique=True, null=True, blank=True)
    language = models.CharField(max_length=3, null=True, blank=True)

    history = HistoricalRecords()


    class Meta:
        ordering = ['definition']
        constraints = [
            models.UniqueConstraint(
                fields=['definition', 'language'], name='definition_language'
            )
        ]

    def __str__(self):
        return '{}'.format(self.definition)
