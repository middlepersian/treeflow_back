from distutils.command.config import LANG_EXT
import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .language import LanguageChoices


class Translation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    language = models.CharField(max_length=3, choices=LanguageChoices.choices, null=True, blank=True)
    text = models.TextField(null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['text']
        constraints = [
            models.UniqueConstraint(
                fields=['language', 'text'], name='translation_language_text'
            )
        ]

    def __str__(self):
        return self.text
