import uuid as uuid_lib
from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords


class Lemma(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    word = models.CharField(max_length=100)
    language = models.CharField(max_length=3, null=True, blank=True)
    multiword_expression = models.BooleanField(default=False)
    related_lemmas = models.ManyToManyField('self', blank=True, related_name="lemma_related_lemmas",through='LemmaRelation')
    related_meanings = models.ManyToManyField('Meaning', blank=True, related_name='lemma_related_meanings', through='LemmaMeaning')

    history = HistoricalRecords()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['word', 'language'], name='word_language_lemma'
            )
        ]
        indexes = [
            models.Index(fields=['word', 'language']),
        ]
        ordering = ['word']



class LemmaRelation(models.Model):
    lemma1 = models.ForeignKey(Lemma, on_delete=models.CASCADE, related_name='related_lemmas1')
    lemma2 = models.ForeignKey(Lemma, on_delete=models.CASCADE, related_name='related_lemmas2')
    # eg hypernymy, hyponymy, meronymy, holonymy, synonymy, antonymy, etc.
    relation_type = models.CharField(max_length=50, null=True, blank=True)
    history = HistoricalRecords()
   
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['lemma1', 'lemma2'], name='lemma_relation'
            )
        ]
        indexes = [
            models.Index(fields=['lemma1', 'lemma2']),
        ]

class LemmaMeaning(models.Model):
    lemma = models.ForeignKey(Lemma, on_delete=models.CASCADE, related_name='related_lemma')
    meaning = models.ForeignKey('Meaning', on_delete=models.CASCADE, related_name='related_meaning')    
    history = HistoricalRecords()
   
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['lemma', 'meaning'], name='lemma_meaning'
            )
        ]
        indexes = [
            models.Index(fields=['lemma', 'meaning']),
        ]        