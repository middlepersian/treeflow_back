from django.db.models.deletion import CASCADE
from mpcd.corpus.models.token import Token
import uuid as uuid_lib
from django.db import models
from django.db.models.fields.related import ForeignKey
from .edition import Edition
from .token import Token
from .codex import Codex, CodexToken
from .sigle import TextSigle
from .author import Author
from simple_history.models import HistoricalRecords


class StageCh(models.TextChoices):
    untouched = 'UNT', 'untouched'
    in_progess = 'IPR', 'in_progress'
    finished = 'FIN', 'finished'


class Resource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    project = models.TextField(blank=True)
    reference = models.URLField(blank=True, null=True)


class Text(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=100)
    text_sigle = models.ForeignKey(TextSigle, on_delete=models.CASCADE, null=True)

    description = models.CharField(max_length=255, blank=True)
    resource = ForeignKey(Resource, on_delete=models.CASCADE, null=True, blank=True)
    stage = models.CharField(max_length=3, blank=True, choices=StageCh.choices, default=StageCh.untouched)

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                name="valid_stage",
                check=models.Q(stage__in=StageCh.values),
            )]

    def __str__(self):
        return '{}'.format(self.name)


class Sentence(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    text = models.ForeignKey(Text, on_delete=models.CASCADE, null=True, blank=True)
    tokens = models.ManyToManyField(Token)

    comment = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True

    def get_tokens(self):
        return "|".join([p.transcription for p in self.tokens.all()])


# CODEX_TEXT
class CodexText(Text):
    codex = models.ForeignKey(Codex, on_delete=models.CASCADE)
    editor = models.ForeignKey(Author, on_delete=CASCADE, blank=True, related_name='editor_codex')
    collaborator = models.ManyToManyField(Author, blank=True, related_name='collaborator_codex')

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="valid_stage_codex",
                check=models.Q(stage__in=StageCh.values),
            )]

    def __str__(self):
        return '{} {} {}'.format(self.name, self.codex, self.text_sigle)


class CodexSentence(Sentence):

    text = models.ForeignKey(CodexText, on_delete=models.CASCADE, null=True, blank=True)
    tokens = models.ManyToManyField(CodexToken)


# EDITION_TEXT
class EditionText(Text):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    editor = models.ForeignKey(Author, on_delete=CASCADE, blank=True, related_name='editor_edition')
    collaborator = models.ManyToManyField(Author, blank=True, related_name='collaborator_edition')

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="valid_stage_edition",
                check=models.Q(stage__in=StageCh.values),
            )]

    def __str__(self):
        return '{} {} {}'.format(self.name, self.edition, self.text_sigle)


class EditionSentence(Sentence):
    text = models.ForeignKey(EditionText, on_delete=models.CASCADE, null=True, blank=True)
