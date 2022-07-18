from django.db import models
from simple_history.models import HistoricalRecords
from .source import Source


class Codex(Source):
    sigle = models.CharField(max_length=5, unique=True)
    comments = models.ManyToManyField('Comment', blank=True, related_name = 'codex_comments')

    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.sigle)
