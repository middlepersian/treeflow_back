from django.db import models
from simple_history.models import HistoricalRecords
from .source import Source


class Codex(Source):
    sigle = models.CharField(max_length=5, unique=True)
    comment = models.ForeignKey('Comment', on_delete=models.SET_NULL, null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.sigle)
