import uuid as uuid_lib
from django.db import models
from django.urls import reverse
from .physical import Codex, CodexToken
from .token import Token
from simple_history.models import HistoricalRecords


class TextSigle(models.TextChoices):
    DMX = 'DMX', 'DMX'
    ENN = 'ENN', 'ENN'



class Text(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    codex = models.ForeignKey(Codex, on_delete=models.CASCADE)
    text_sigle = models.CharField(choices=TextSigle.choices, max_length=4, null=True)
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=255, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.name)


class Section(models.Model):
    SENTENCE = 'SEN'
    CHAPTER = 'CHA'
    VERSE = 'VER'
    STROPHE = 'STR'

    SECTION_TYPE = (
        (SENTENCE, 'Sentence'),
        (CHAPTER, 'Chapter'),
        (VERSE, 'Verse'),
        (STROPHE, 'Strophe'),
    )

    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    section_type = models.CharField(max_length=3, choices=SECTION_TYPE, null=True)
    comment = models.CharField(max_length=255, blank=True)
    text = models.ForeignKey(Text, on_delete=models.CASCADE, blank=True, null=True)
    section_container = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='section', blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.text, self.section_type)


class TokenContainer(models.Model):
    SENTENCE = 'SEN'
    PARAGRAPH = 'PAR'
    CLAUSE = 'CLA'
    PHRASE = 'PHR'

    CONTAINER_TYPE = (
        (SENTENCE, 'Sentence'),
        (PARAGRAPH, 'Paragraph'),
        (CLAUSE, 'Clause'),
        (PHRASE, 'Phrase')
    )

    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    container_type = models.CharField(max_length=3, choices=CONTAINER_TYPE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)

    comment = models.CharField(max_length=255, blank=True)
    tokens = models.ManyToManyField(CodexToken)
    history = HistoricalRecords()


    def get_tokens(self):
        return "|".join([p.transcription for p in self.tokens.all()])    

    def __str__(self):
        return '{} {}'.format(self.container_type, self.section)
