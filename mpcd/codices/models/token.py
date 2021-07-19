import uuid as uuid_lib

from django.db import models
from django.urls import reverse
from physical import Line


class Token(models.Model):
    tkn = models.CharField(max_length=255)
    trascription = models.TextField(blank=True)
    transliteration = models.TextField(blank=True)
    lemma = models.ForeignKey()
    annotations =models.ForeignKey()
    line_id = models.ForeignKey(Line, on_delete=models.SET_NULL) 

