import uuid as uuid_lib
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from simple_history.models import HistoricalRecords
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager
class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    number = models.FloatField(null=True, blank=True)
    number_in_sentence = models.FloatField(blank=True, null=True)

    root = models.BooleanField(default=False)
    word_token = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)

    text = models.ForeignKey('Text', on_delete=models.CASCADE, null=True, blank=True, related_name='token_text')

    language = models.CharField(max_length=3, null=True, blank=True)
    transcription = models.CharField(max_length=50)
    transliteration = models.CharField(max_length=50, blank=True)
    lemmas = models.ManyToManyField('dict.Lemma', blank=True, through='TokenLemma', related_name='token_lemmas')
    meanings = models.ManyToManyField('dict.Meaning', blank=True, through='TokenMeaning', related_name='token_meanings')

    avestan = models.TextField(null=True, blank=True)

    previous = models.OneToOneField('self',
                                    related_name='next',
                                    blank=True,
                                    null=True,
                                    on_delete=models.SET_NULL, db_index=True)

    gloss = models.TextField(blank=True, null=True)

    multiword_token = models.BooleanField(default=False)
    multiword_token_number = ArrayField(models.FloatField(blank=True, null=True), null=True, blank=True)
    related_tokens = models.ManyToManyField('self', blank=True)

    pos = "RelatedManager[POS]"
    dependencies = "RelatedManager[Dependency]"
    features = "RelatedManager[Feature]"


    history = HistoricalRecords()


    class Meta:
        ordering = ['number']
        constraints = [
            models.UniqueConstraint(
                fields=['number', 'text'], name='token_number_text'
            )
        ]
        indexes = [
            models.Index(fields=['text', 'number', 'transcription', 'transliteration', 'previous'])
        ]

    def __str__(self):
        return '{}'.format(self.transcription)



class TokenLemma(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    lemma = models.ForeignKey('dict.Lemma', on_delete=models.CASCADE)
    class Meta:
        unique_together = ['token', 'lemma']
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['lemma']),
        ]



class TokenMeaning(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    meaning = models.ForeignKey('dict.Meaning', on_delete=models.CASCADE)


    class Meta:
        unique_together = ['token', 'meaning']
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['meaning']),
        ]