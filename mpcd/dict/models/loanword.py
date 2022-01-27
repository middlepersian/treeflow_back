import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .language import Language
from .translation import Translation


class LoanWord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    word = models.CharField(unique=True, max_length=50)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=True,
                                 null=True, related_name='loanword_language')
    translations = models.ManyToManyField(Translation, blank=True, related_name='loanword_translations')

    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.language, self.word)