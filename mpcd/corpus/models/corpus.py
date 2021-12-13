from django.db.models.deletion import CASCADE
from django.utils import translation
from mpcd.corpus.models.token import Token
import uuid as uuid_lib
from django.db import models
from django.db.models.fields.related import ForeignKey
from .edition import Edition
from .token import Token
from .codex import Codex
from .sigle import TextSigle
from .author import Author
from simple_history.models import HistoricalRecords


class Corpus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=10, unique=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class StageCh(models.TextChoices):
    untouched = 'UNT', 'untouched'
    in_progess = 'PRO', 'in_progress'
    finished = 'FIN', 'finished'


class Resource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)
    project = models.TextField(blank=True)
    reference = models.URLField(blank=True, null=True)


class Text(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    corpus = models.ForeignKey(Corpus, on_delete=CASCADE, null=True, blank=True)

    title = models.CharField(max_length=100)
    text_sigle = models.ForeignKey(TextSigle, on_delete=models.CASCADE, null=True)

    editor = models.ForeignKey(Author, on_delete=CASCADE, blank=True, related_name='editor_text')
    collaborator = models.ManyToManyField(Author, blank=True, related_name='collaborator_text')

    resource = ForeignKey(Resource, on_delete=models.CASCADE, null=True, blank=True)
    stage = models.CharField(max_length=3, blank=True, choices=StageCh.choices, default=StageCh.untouched)

    # in corpus.rng a text can have as source a single "edition" or a single "codex". We will leave it a bit more flexible.
    codex_source = models.ManyToManyField(Codex,  blank=True)
    edition_source = models.ManyToManyField(Edition,  blank=True)

    history = HistoricalRecords(inherit=True)

    class Meta:
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

    translation = models.TextField(null=True, blank=True)
    comment = models.CharField(max_length=255, blank=True)

    history = HistoricalRecords(inherit=True)

    def get_tokens(self):
        return "|".join([p.transcription for p in self.tokens.all()])
