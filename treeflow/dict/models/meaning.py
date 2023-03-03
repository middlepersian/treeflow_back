import uuid as uuid_lib
from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from treeflow.corpus.models.comment import Comment
from treeflow.dict.models.lemma import Lemma


class Meaning(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    meaning = models.TextField(null=True, blank=True, db_index=True)
    language = models.CharField(max_length=10, blank=True, null=True, db_index=True)
    related_meanings = models.ManyToManyField('self', blank=True, related_name='meaning_related_meanings')
    created_at = models.DateTimeField(auto_now_add=True)


    def related_lemmas(self):
            return self.lemma_related_meanings.all()
            
    history = HistoricalRecords()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['meaning', 'language'], name='meaning_language_meaning'
            )]
        ordering = ['meaning']
        indexes = [
            models.Index(fields=['meaning', 'language']),
        ]

    def __str__(self):
        return '{} {}'.format(self.meaning, self.language)
