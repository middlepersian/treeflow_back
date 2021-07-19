from app_backend.mpcd.codices.models.token import Token
import uuid as uuid_lib
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from enum import Enum
from physical import Codex
from token import Token


class Text(models.Model):
    class TextType(Enum):
        prose = ('pr', 'Prose')
        lyric = ('ly', 'Lyric')
    text_type = models.CharField(max_length=2, choices=[x.value for x in TextType])    
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    codex_id = models.ForeignKey(Codex)


## Prose

class Chapter (models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    text_id = models.ForeignKey(Text)

class Section (models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    chapter_id = models.ForeignKey(Chapter)

class Sentence (models. Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    section_id = models.ForeignKey(Chapter)
    tokens =  ArrayField(Token)   


## Lyric

class Strophe (models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    text_id = models.ForeignKey(Text)

class Verse (models. Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    verse_id = models.ForeignKey(Strophe)
    tokens =  ArrayField(Token)   
