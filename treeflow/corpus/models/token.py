import uuid as uuid_lib
from django.db import models
from django.contrib.postgres.fields import ArrayField
from simple_history.models import HistoricalRecords
from treeflow.utils.normalize import strip_and_normalize

class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    number = models.FloatField(null=True, blank=True)
    number_in_sentence = models.FloatField(blank=True, null=True)

    root = models.BooleanField(default=False)
    word_token = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)

    text = models.ForeignKey('Text', on_delete=models.CASCADE, null=True, blank=True, related_name='token_text')
    image = models.ForeignKey('images.Image', on_delete=models.CASCADE, null=True, blank=True, related_name='token_image')

    language = models.CharField(max_length=3, null=True, blank=True)
    transcription = models.TextField(null=True, blank=True)
    transliteration = models.TextField(null=True, blank=True)
    lemmas = models.ManyToManyField('dict.Lemma', blank=True, through='TokenLemma', related_name='token_lemmas')
    senses = models.ManyToManyField('dict.Sense', blank=True, through='TokenSense', related_name='token_senses')

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
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()


    class Meta:
        ordering = ['number']
        constraints = [
            models.UniqueConstraint(
                fields=['text', 'number'], name='token_text_number'
            )
        ]
        indexes = [
            models.Index(fields=['transcription']),
            models.Index(fields=['transliteration']),
            models.Index(fields=['number']),
        ]

    def __str__(self):
        return '{}'.format(self.transcription)
    
    def save(self, *args, **kwargs):
        #normalize transcription
        if self.transcription:
            self.transcription = strip_and_normalize('NFC', self.transcription)

        #normalize transliteration
        if self.transliteration:
            self.transliteration = strip_and_normalize('NFC', self.transliteration)

        #normalize language
        if self.language:
            #lowercase
            self.language = self.language.strip().lower()    

        #normalize avestan
        if self.avestan:
            self.avestan = strip_and_normalize('NFC', self.avestan)

        #normalize gloss
        if self.gloss:
            self.gloss = strip_and_normalize('NFC', self.gloss)

        #save
        super().save(*args, **kwargs)



class TokenLemma(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    lemma = models.ForeignKey('dict.Lemma', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['token', 'lemma']
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['lemma']),
        ]


class TokenSense(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    sense = models.ForeignKey('dict.Sense', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ['token', 'sense']
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['sense']),
        ]        