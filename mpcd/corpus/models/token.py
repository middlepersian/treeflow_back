import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .dependency import Dependency
from .morphological_annotation import MorphologicalAnnotation
from .text import Text
from .line import Line
from .token_comment import TokenComment


class Token(models.Model):
    # TODO
    #root = BooleanField()
    #word_token = BooleanField()
    #visible = BooleanField()
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    number = models.FloatField(null=True, blank=True)
    text = models.ForeignKey(Text, on_delete=models.CASCADE, null=True, blank=True, related_name='token_text')
    language = models.CharField(max_length=3, null=True, blank=True)
    transcription = models.CharField(max_length=50)
    transliteration = models.CharField(max_length=50, blank=True)
    lemmas = models.ManyToManyField('dict.Lemma', blank=True, related_name='token_lemmas')
    meanings = models.ManyToManyField('dict.Meaning', blank=True, related_name='token_meanings')
    pos = models.CharField(max_length=8, null=True, blank=True)
    morphological_annotation = models.ManyToManyField(
        MorphologicalAnnotation, blank=True, related_name='token_morphological_annotation')
    syntactic_annotation = models.ManyToManyField(Dependency, blank=True, related_name="token_syntactic_annotation")

    comments = models.ManyToManyField(TokenComment, blank=True, related_name="token_comments")

    avestan = models.TextField(null=True, blank=True)

    line = models.ForeignKey(Line, on_delete=models.SET_NULL, null=True, related_name='token_line')

    previous = models.OneToOneField('self',
                                    related_name='next',
                                    blank=True,
                                    null=True,
                                    on_delete=models.SET_NULL)

    gloss = models.TextField(blank=True, null=True)

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
