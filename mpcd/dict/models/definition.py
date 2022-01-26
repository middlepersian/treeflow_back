import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .language import Language


class Definition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    definition = models.TextField(unique=True, null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=True,
                                 null=True, related_name='definition_language')
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.definition)
