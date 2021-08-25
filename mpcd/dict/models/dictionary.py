import uuid as uuid_lib

from django.db import models
from django.db.models.expressions import F
from django.db.models.fields import SlugField
from django.urls import reverse




class PhoneticVariants(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    
    
class Entry(models.Model):
    uuid = models.UUIDField(default = uuid_lib.uuid4, editable=False, unique=True)
    doi = models.URLField(max_length=200)
    lemma = models.CharField(unique=True)
    phonetic_variants = models.ForeignKey(PhoneticVariants)


class Dictionary(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=10)
    entry = models.ForeignKey(Entry)


