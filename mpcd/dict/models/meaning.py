import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .language import LanguageChoices


class Meaning(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    meaning = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=10, choices=LanguageChoices.choices)
    #relationships
    related_meanings = models.ManyToManyField('self', blank=True, related_name='meaning_related_meanings')
    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['meaning', 'language'], name='meaning_language_meaning'
            )]
        ordering = ['meaning']

    def __str__(self):
        return '{}'.format(self.meaning)
