import uuid as uuid_lib
from django.db import models
from django.urls import reverse
from .physical import Codex, CodexToken
from .token import Token
from simple_history.models import HistoricalRecords

class TextSigle(models.TextChoices):
    pass


class Text(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    codex = models.ForeignKey(Codex, on_delete=models.CASCADE)
    text_sigle = models.CharField(choices=TextSigle.choices, max_length=4, null=True)
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=255, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.text_type, self.name)


# Prose

class Chapter (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True)
    comment = models.CharField(max_length=255, blank=True)

    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    history = HistoricalRecords()


    def __str__(self):
        return '{}'.format(self.name)


class Section (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    comment = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.name)


class Sentence (models. Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, blank=True)
    tokens = models.ManyToManyField(CodexToken)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.tokens)


# Lyric

class Strophe (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.id)


class Verse (models. Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    verse = models.ForeignKey(Strophe, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, blank=True)
    tokens = models.ManyToManyField(CodexToken)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.tokens)
