from .resource import Resource
from .source import Source
from .text_sigle import TextSigle
from .corpus import Corpus
from django.db import models
import uuid as uuid_lib
from simple_history.models import HistoricalRecords
from django.contrib.auth import get_user_model
User = get_user_model()


class StageCh(models.TextChoices):
    untouched = 'UNT', 'untouched'
    in_progess = 'PRO', 'in_progress'
    finished = 'FIN', 'finished'


class Text(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, null=True, blank=True, related_name='text_corpus')

    title = models.CharField(max_length=100, unique=True)
    text_sigle = models.ForeignKey(TextSigle, on_delete=models.SET_NULL, null=True, related_name='text_text_sigle')

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
        return '{}'.format(self.title)
