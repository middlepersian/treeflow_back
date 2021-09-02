import uuid as uuid_lib
from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords

from mpcd.codex.models.token import Token

class Edition(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    description = models.TextField(blank=True)
    history = HistoricalRecords()


class Text(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    edition_id = models.ForeignKey(Edition, on_delete=models.CASCADE)
    history = HistoricalRecords()

class Chapter (models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    text_id = models.ForeignKey(Text, on_delete=models.CASCADE)
    history = HistoricalRecords()

class Section (models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    chapter_id = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    history = HistoricalRecords()

class Sentence (models. Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    tokens =  models.ForeignKey(Token, on_delete=models.CASCADE, related_name='edition_tokens') 
    history = HistoricalRecords()   