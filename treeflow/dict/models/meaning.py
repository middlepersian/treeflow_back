import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from treeflow.corpus.models.comment import Comment


class Meaning(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    meaning = models.TextField(null=True, blank=True, db_index=True)
    language = models.CharField(max_length=10, blank=True, null=True, db_index=True)
    related_meanings = models.ManyToManyField('self', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['meaning', 'language'], name='meaning_language_meaning'
            )]
        ordering = ['meaning']

    def __str__(self):
        return '{} {}'.format(self.meaning, self.language)
