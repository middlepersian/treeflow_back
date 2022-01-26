from .resource import Resource
from .source import Source
from .text_sigle import TextSigle
from .token import Token
from django.db import models
import uuid as uuid_lib
from simple_history.models import HistoricalRecords
from django.contrib.auth import get_user_model
User = get_user_model()


class CorpusManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Corpus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=10, unique=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.slug


class StageCh(models.TextChoices):
    untouched = 'UNT', 'untouched'
    in_progess = 'PRO', 'in_progress'
    finished = 'FIN', 'finished'


class Text(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, null=True, blank=True, related_name='text_corpus')

    title = models.CharField(max_length=100)
    text_sigle = models.ForeignKey(TextSigle, on_delete=models.CASCADE, null=True, related_name='text_text_sigle')

    editors = models.ManyToManyField(User, blank=True, related_name="text_editors")
    collaborators = models.ManyToManyField(User, blank=True, related_name="text_collaborators")

    resources = models.ManyToManyField(Resource, blank=True, related_name='text_resources')
    stage = models.CharField(max_length=3, blank=True, choices=StageCh.choices, default=StageCh.untouched)

    sources = models.ManyToManyField(Source, blank=True, related_name='text_sources')

    history = HistoricalRecords(inherit=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="valid_stage",
                check=models.Q(stage__in=StageCh.values),
            )]

    def __str__(self):
        return '{} {}'.format(self.title, self.text_sigle.sigle)


class Sentence(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    text = models.ForeignKey(Text, on_delete=models.CASCADE, null=True, blank=True, related_name='sentence_text')
    tokens = models.ManyToManyField(Token, related_name='sentence_tokens')

    translation = models.TextField(null=True, blank=True)
    comment = models.CharField(max_length=255, blank=True)

    history = HistoricalRecords(inherit=True)

    def get_tokens(self):
        return "|".join([p.transcription for p in self.tokens.all()])
