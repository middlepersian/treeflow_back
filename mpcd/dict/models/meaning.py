import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords

from .language import LanguageChoices


class Meaning(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    meaning = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=10, choices=LanguageChoices.choices)
    history = HistoricalRecords()
