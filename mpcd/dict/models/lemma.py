import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .meaning import Meaning
from mpcd.corpus.models.comment import Comment


class Lemma(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    word = models.CharField(max_length=100)
    language = models.CharField(max_length=3, null=True, blank=True)
    related_lemmas = models.ManyToManyField('self', blank=True)
    related_meanings = models.ManyToManyField(Meaning, blank=True, related_name='lemma_related_meanings')
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['word', 'language'], name='word_language_lemma'
            )
        ]
        ordering = ['word']

    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.word)
