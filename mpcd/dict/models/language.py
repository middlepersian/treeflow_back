import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords

# TODO place language where required in order to reduce db calls


class LanguageChoices(models.TextChoices):
    # iso 639-3
    akk = 'akk', 'Akkadian'
    ara = 'ara', 'Arabic'
    arc = 'arc', 'Imperial Aramaic (700-300 BCE), Official Aramaic (700-300 BCE)'
    ave = 'ave', 'Avestan'
    eng = 'eng', 'English'
    deu = 'deu', 'German'
    guj = 'guj', 'Gujarati'
    fra = 'fra', 'French'
    grc = 'grc', 'Ancient Greek (to 1453)'
    ita = 'ita', 'Italian'
    pal = 'pal', 'Pahlavi'
    san = 'san', 'Sanskrit'
    spa = 'spa', 'Spanish'
    xpr = 'xpr', 'Parthian'
