import uuid as uuid_lib

from django.db import models
from django.db.models.fields import SlugField
from django.urls import reverse
from simple_history.models import HistoricalRecords



class Dictionary(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=10)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name


    
class Entry(models.Model):
    uuid = models.UUIDField(default = uuid_lib.uuid4, editable=False, unique=True)
    lemma = models.CharField(unique=True, max_length=30)
    dict = models.ForeignKey(Dictionary, on_delete=models.CASCADE, blank=True)
    doi = models.URLField(max_length=200, null=True, blank=True)
    history = HistoricalRecords()



    def __str__(self):
        return self.lemma




