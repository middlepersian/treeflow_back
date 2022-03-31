import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib import admin
from mpcd.dict.models import Entry
from .dependency import Dependency
from .morphological_annotation import MorphologicalAnnotation
from .pos import POSChoices
from .text import Text
from .line import Line
from .comment_category import CommentCategory

from mpcd.dict.models.language import LanguageChoices


class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    number = models.FloatField(null=True, blank=True)
    text = models.ForeignKey(Text, on_delete=models.CASCADE, null=True, blank=True, related_name='token_text')
    language = models.CharField(max_length=3, choices=LanguageChoices.choices, null=True, blank=True)
    transcription = models.CharField(max_length=50)
    transliteration = models.CharField(max_length=50, blank=True)
    entries = models.ManyToManyField(Entry, blank=True, related_name='token_entries')
    pos = models.CharField(max_length=8, choices=POSChoices.choices, null=True, blank=True)
    morphological_annotation = models.ManyToManyField(
        MorphologicalAnnotation, blank=True, related_name='token_morphological_annotation')
    syntactic_annotation = models.ManyToManyField(Dependency, blank=True, related_name="token_syntactic_annotation")
    comment = models.TextField(blank=True)
    comment_uncertain = models.ManyToManyField(CommentCategory, blank=True, related_name='token_comment_uncertain')
    comment_to_discuss = models.ManyToManyField(CommentCategory, blank=True, related_name='token_comment_to_discuss')
    comment_new_suggestion = models.ManyToManyField(
        CommentCategory, blank=True, related_name='token_comment_new_suggestion')

    avestan = models.URLField(max_length=100, null=True, blank=True)

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
