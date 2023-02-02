import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .meaning import Meaning
from treeflow.corpus.models.comment import Comment


class Lemma(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    word = models.CharField(max_length=100)
    language = models.CharField(max_length=3, null=True, blank=True)
    related_lemmas = models.ManyToManyField('self', blank=True)
    related_meanings = models.ManyToManyField(Meaning, blank=True, related_name='lemma_related_meanings')

    def get_related_lemmas(self):
        return " | ".join([p.word for p in self.related_lemmas.all()])
    def get_related_meanings(self):
        return " | ".join([p.meaning for p in self.related_meanings.all()])
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['word', 'language'], name='word_language_lemma'
            )
        ]
        ordering = ['word']

    history = HistoricalRecords()

    def __str__(self):
        return '{} {} - {} {}'.format(self.word, self.language, self.get_related_lemmas(), self.get_related_meanings())
