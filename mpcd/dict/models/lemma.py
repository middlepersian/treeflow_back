import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .language import LanguageChoices
from .loanword import LoanWord


class Lemma(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    word = models.CharField(max_length=100)
    language = models.CharField(max_length=3, choices=LanguageChoices.choices, null=True, blank=True)
    loanwords = models.ManyToManyField(LoanWord, blank=True, related_name='lemma_loanwords')
    related_lemmas = models.ManyToManyField('self', blank=True, related_name='lemma_related_lemmas')
    comment = models.TextField(null=True, blank=True)


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
