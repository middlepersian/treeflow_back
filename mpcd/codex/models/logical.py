import uuid as uuid_lib
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from .physical import Codex
from .token import Token
from simple_history.models import HistoricalRecords



class TextType(models.TextChoices):
    PROSE = 'P'
    LYRIC = 'L'


class Text(models.Model):
    text_type = models.CharField(choices=TextType.choices, max_length=1)
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    codex_id = models.ForeignKey(Codex, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.text_type, self.uuid)


# Prose

class Chapter (models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    text_id = models.ForeignKey(Text, on_delete=models.CASCADE)
    history = HistoricalRecords()


    def __str__(self):
        return '{}'.format(self.uuid)


class Section (models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    chapter_id = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.uuid)


class Sentence (models. Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    tokens = models.ForeignKey(Token, on_delete=models.CASCADE, related_name='prose_tokens')
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.uuid)


# Lyric

class Strophe (models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    text_id = models.ForeignKey(Text, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.uuid)


class Verse (models. Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    verse_id = models.ForeignKey(Strophe, on_delete=models.CASCADE)
    tokens = models.ForeignKey(Token, on_delete=models.CASCADE, related_name='lyric_tokens')
    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.uuid)
