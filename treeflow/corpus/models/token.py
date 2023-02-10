import uuid as uuid_lib
from django.db import models
from django.contrib.postgres.fields import ArrayField
from simple_history.models import HistoricalRecords


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
    lemmas = models.ManyToManyField('dict.Lemma', blank=True, related_name='token_lemmas')
    meanings = models.ManyToManyField('dict.Meaning', blank=True, related_name='token_meanings')
    upos = models.CharField(max_length=8, null=True, blank=True)
    xpos = ArrayField(models.CharField(max_length=8), null=True, blank=True)
    postfeatures = models.ManyToManyField(
        'PostFeature', blank=True, related_name='token_postfeatures')
    dependencies = models.ManyToManyField('Dependency', blank=True, related_name="token_dependencies")

    avestan = models.TextField(null=True, blank=True)

    previous = models.OneToOneField('self',
                                    related_name='next',
                                    blank=True,
                                    null=True,
                                    on_delete=models.SET_NULL)

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
