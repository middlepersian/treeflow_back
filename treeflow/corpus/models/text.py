from typing import TYPE_CHECKING
from django.contrib.postgres.fields import ArrayField
from strawberry.lazy_type import LazyType
from django.db import models
import uuid as uuid_lib
from simple_history.models import HistoricalRecords
from django.conf import settings

from .bibliography import BibEntry
from .source import Source
from .corpus import Corpus



class Text(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, null=True, blank=True, related_name='text_corpus')
    title = models.CharField(max_length=100, null=True, blank=True)
    identifier = models.CharField(max_length=20, null=True, blank=True)
    language = ArrayField(models.CharField(max_length=3), blank=True, null=True)
    #e.g. sigle
    series = models.CharField(max_length=20, null=True,blank=True)
    # e.g. genre
    label = models.CharField(max_length=20, null=True, blank=True)
    stage = models.CharField(max_length=10, blank=True)
    
    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="text_editors")
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="text_collaborators")
   
    # a any source that should be documented in Zotero
    sources = models.ManyToManyField(Source, blank=True, related_name='text_sources')
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']
        constraints = [
            models.UniqueConstraint(
                fields=['corpus', 'identifier'], name='text_corpus_identifier'
            )
        ]



