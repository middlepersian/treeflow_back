import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords

## TODO place language where required in order to reduce db calls
class LanguageChoices(models.TextChoices):
    # iso 639-3
    akk = 'akk', 'Akkadian'
    arc = 'arc', 'Imperial Aramaic (700-300 BCE), Official Aramaic (700-300 BCE)'
    ave = 'ave', 'Avestan'
    eng = 'eng', 'English'
    deu = 'deu', 'German'
    fra = 'fra', 'French'
    grc = 'grc', 'Ancient Greek (to 1453)'
    ita = 'ita', 'Italian'
    pal = 'pal', 'Pahlavi'
    spa = 'spa', 'Spanish'
    xpr = 'xpr', 'Parthian'


class Language(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    identifier = models.CharField(max_length=3, choices=LanguageChoices.choices, unique=True)
    history = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.identifier)
