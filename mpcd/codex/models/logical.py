import uuid as uuid_lib
from django.db import models
from django.urls import reverse
from .physical import Codex, CodexToken
from .token import Token
from simple_history.models import HistoricalRecords



class TextType(models.TextChoices):
    PROSE = 'P'
    LYRIC = 'L'


class Text(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    text_type = models.CharField(choices=TextType.choices, max_length=1)
    name = models.CharField(max_length=100, null=True)
    codex = models.ForeignKey(Codex, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.text_type, self.name)


# Prose

class Chapter (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True)
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    history = HistoricalRecords()


    def __str__(self):
        return '{}'.format(self.name)


class Section (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.name)


class Sentence (models. Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    tokens = models.ManyToManyField(CodexToken)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.tokens)


# Lyric

class Strophe (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.id)


class Verse (models. Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    verse = models.ForeignKey(Strophe, on_delete=models.CASCADE)
    tokens = models.ManyToManyField(CodexToken)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.tokens)
