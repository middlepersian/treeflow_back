import uuid as uuid_lib
from typing import TYPE_CHECKING
from django.db import models
from simple_history.models import HistoricalRecords
from mpcd.corpus.models.codex import Codex


class CodexPart(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    codex = models.ForeignKey(Codex, on_delete=models.SET_NULL, related_name='codex_part_codex', null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    comments = models.ManyToManyField('Comment', blank=True, related_name='codex_part_comments')

    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.slug)
