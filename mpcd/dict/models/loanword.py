import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .language import LanguageChoices
from .translation import Translation


class LoanWord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    word = models.CharField(unique=True, max_length=50)
    language = models.CharField(max_length=3, choices=LanguageChoices.choices, null=True, blank=True)

    translations = models.ManyToManyField(Translation, blank=True, related_name='loanword_translations')

    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['word', 'language'], name='word_language_loanword'
            )
        ]
        ordering = ['word']

    def __str__(self):
        return '{} {}'.format(self.language, self.word)
