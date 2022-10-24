from typing import TYPE_CHECKING
from strawberry.lazy_type import LazyType
from django.db import models
import uuid as uuid_lib
from simple_history.models import HistoricalRecords
from django.contrib.auth import get_user_model

from .bibliography import BibEntry
from .source import Source
from .text_sigle import TextSigle
from .corpus import Corpus

User = get_user_model()

class Text(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, null=True, blank=True, related_name='text_corpus')
    title = models.CharField(max_length=100, unique=True)
    text_sigle = models.ForeignKey(TextSigle, on_delete=models.SET_NULL, null=True, related_name='text_text_sigle')
    editors = models.ManyToManyField(User, blank=True, related_name="text_editors")
    collaborators = models.ManyToManyField(User, blank=True, related_name="text_collaborators")
    stage = models.CharField(max_length=3, blank=True)
    # a Source can be a "Codex" or an "Edition"
    sources = models.ManyToManyField(Source, blank=True, related_name='text_sources')
    # a Resource can be any Zotero reference
    resources = models.ManyToManyField(BibEntry, blank=True, related_name='text_resources')
    history = HistoricalRecords(inherit=True)

    ## TODO: add comment

    class Meta:
        constraints = [

            models.UniqueConstraint(
                fields=['corpus', 'title'], name='corpus_title'
            )
        ]

    def __str__(self):
        return '{}'.format(self.title)
