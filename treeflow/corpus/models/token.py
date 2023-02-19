import uuid as uuid_lib
from django.db import models
from django.contrib.postgres.fields import ArrayField
from simple_history.models import HistoricalRecords


class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    number = models.FloatField(null=True, blank=True,  db_index=True)
    number_in_sentence = models.FloatField(blank=True, null=True)

    root = models.BooleanField(default=False)
    word_token = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)

    text = models.ForeignKey('Text', on_delete=models.CASCADE, null=True, blank=True, related_name='token_text', db_index=True)

    language = models.CharField(max_length=3, null=True, blank=True)
    transcription = models.CharField(max_length=50,  db_index=True)
    transliteration = models.CharField(max_length=50, blank=True,  db_index=True)
    lemmas = models.ManyToManyField('dict.Lemma', blank=True, related_name='token_lemmas', through='TokenLemma', db_index=True)
    meanings = models.ManyToManyField('dict.Meaning', blank=True, related_name='token_meanings', through='TokenMeaning', db_index=True)
    upos = models.CharField(max_length=8, null=True, blank=True)
    xpos = ArrayField(models.CharField(max_length=8), null=True, blank=True)
    features = models.ManyToManyField('Feature', blank=True, related_name='token_features', through='TokenFeature', db_index=True)
    dependencies = models.ManyToManyField('Dependency', blank=True, related_name="token_dependencies", through='TokenDependency', db_index=True)
    avestan = models.TextField(null=True, blank=True)

    previous = models.OneToOneField('self',
                                    related_name='next',
                                    blank=True,
                                    null=True,
                                    on_delete=models.SET_NULL, db_index=True)

    gloss = models.TextField(blank=True, null=True)

    multiword_token = models.BooleanField(default=False)
    multiword_token_number = ArrayField(models.FloatField(blank=True, null=True), null=True, blank=True)
    related_tokens = models.ManyToManyField('self', blank=True, related_name='token_related_tokens')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['number']
        constraints = [
            models.UniqueConstraint(
                fields=['number', 'text'], name='token_number_text'
            )
        ]

    def __str__(self):
        return '{}'.format(self.transcription)



class TokenLemma(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    lemma = models.ForeignKey('dict.Lemma', on_delete=models.CASCADE)
    # other fields...

class TokenMeaning(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    meaning = models.ForeignKey('dict.Meaning', on_delete=models.CASCADE)
    # other fields...

class TokenFeature(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    feature = models.ForeignKey('Feature', on_delete=models.CASCADE)
    # other fields...

class TokenDependency(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    dependency = models.ForeignKey('Dependency', on_delete=models.CASCADE)