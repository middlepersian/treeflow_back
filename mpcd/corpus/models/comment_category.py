import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords


class CatChoices(models.TextChoices):
    C = 'C', 'Transcription'
    L = 'L', 'Transliteration'
    S = 'S', 'Semantics'
    M = 'M', 'Morphology'
    X = 'X', 'Syntax'


class CommentCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    category = models.CharField(max_length=8, choices=CatChoices.choices, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.category)
