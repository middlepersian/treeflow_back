import uuid as uuid_lib

from django.db import models
from django.db.models.fields import CharField
from django.urls import reverse
from simple_history.models import HistoricalRecords



class Dictionary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=10)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name


class LangCh(models.TextChoices):
    #iso 639-3
    akk = 'akk', 'Akkadian'
    arc = 'arc', 'Imperial Aramaic (700-300 BCE), Official Aramaic (700-300 BCE)'
    ave = 'ave', 'Avestan'
    grc = 'grc', 'Ancient Greek (to 1453)'
    xpr = 'xpr', 'Parthian'

class Lang(models.Model):
    language =  models.CharField(max_length=3, choices=LangCh.choices, unique=True)   
    def __str__(self):
        return '{}'.format(self.language)

class LoanWord(models. Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    word = models.CharField(unique=True, max_length=30, null=True)
    language = models.ForeignKey(Lang, on_delete=models.CASCADE, null=True)

class MeaningEnglish(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    meaning = models.CharField(unique=True, max_length=30)
    history = HistoricalRecords()
    def __str__(self):
        return self.meaning
 
class Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    dict = models.ForeignKey(Dictionary, on_delete=models.CASCADE, blank=True)
    doi = models.URLField(max_length=200, null=True, blank=True)
    lemma = models.CharField(unique=True, max_length=30)
    meaning_en = models.ManyToManyField(MeaningEnglish)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.lemma)




