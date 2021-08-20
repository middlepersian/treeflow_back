import uuid as uuid_lib
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from enum import Enum
from .physical import Codex
from .token import Token


class Text(models.Model):
    class TextType(models.TextChoices):
        PROSE = 'P'
        LYRIC = 'L'
    text_type = models.CharField(choices=TextType.choices, max_length=1)    
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    codex_id = models.ForeignKey(Codex, on_delete=models.CASCADE)


## Prose

class Chapter (models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    text_id = models.ForeignKey(Text, on_delete=models.CASCADE)

class Section (models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    chapter_id = models.ForeignKey(Chapter, on_delete=models.CASCADE)

class Sentence (models. Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    section_id = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    tokens =  models.ForeignKey(Token, on_delete=models.CASCADE)


## Lyric

class Strophe (models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    text_id = models.ForeignKey(Text, on_delete=models.CASCADE)

class Verse (models. Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    verse_id = models.ForeignKey(Strophe, on_delete=models.CASCADE)
    tokens =  models.ForeignKey(Token, on_delete=models.CASCADE)
