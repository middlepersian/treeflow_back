import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from mpcd.corpus.models.comment import Comment


class Meaning(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    meaning = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    # relationships
    related_meanings = models.ManyToManyField('self', blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['meaning', 'language'], name='meaning_language_meaning'
            )]
        ordering = ['meaning']

    def __str__(self):
        return '{}'.format(self.meaning)
