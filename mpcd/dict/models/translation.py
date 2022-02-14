from distutils.command.config import LANG_EXT
import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .language import Language


class Translation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=True,
                                 null=True, related_name='translation_language')
    text = models.TextField(unique=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.text
