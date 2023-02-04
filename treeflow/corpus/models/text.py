from typing import TYPE_CHECKING
from django.contrib.postgres.fields import ArrayField
from strawberry.lazy_type import LazyType
from django.db import models
import uuid as uuid_lib
from simple_history.models import HistoricalRecords
from django.contrib.auth import get_user_model

from .bibliography import BibEntry
from .source import Source
from .corpus import Corpus

User = get_user_model()


class Text(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, null=True, blank=True, related_name='text_corpus')
    title = models.CharField(max_length=100, unique=True)
    language = ArrayField(models.CharField(max_length=3), blank=True, null=True)
    #e.g. sigle
    series = models.CharField(max_length=20, null=True,blank=True)
    # e.g. genre
    label = models.CharField(max_length=20, null=True, blank=True)
    stage = models.CharField(max_length=10, blank=True)
    
    editors = models.ManyToManyField(User, blank=True, related_name="text_editors")
    collaborators = models.ManyToManyField(User, blank=True, related_name="text_collaborators")
   
    # a any source that should be documented in Zotero
    sources = models.ManyToManyField(Source, blank=True, related_name='text_sources')

    history = HistoricalRecords()

    # TODO: add comment

    class Meta:
        constraints = [

            models.UniqueConstraint(
                fields=['corpus', 'title'], name='corpus_title'
            )
        ]

    def __str__(self):
        return '{}'.format(self.title)
