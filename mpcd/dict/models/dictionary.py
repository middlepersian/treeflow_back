import uuid as uuid_lib

from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords



class Dictionary(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=10)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name


class MeaningEnglish(models.Model):
    uuid = models.UUIDField(default = uuid_lib.uuid4, editable=False, unique=True)
    meaning = models.CharField(unique=True, max_length=30)
    history = HistoricalRecords()
    def __str__(self):
        return self.meaning
 
class Entry(models.Model):
    uuid = models.UUIDField(default = uuid_lib.uuid4, editable=False, unique=True)
    dict = models.ForeignKey(Dictionary, on_delete=models.CASCADE, blank=True)
    doi = models.URLField(max_length=200, null=True, blank=True)
    lemma = models.CharField(unique=True, max_length=30)
    meaning_en = models.ManyToManyField(MeaningEnglish)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.lemma)




