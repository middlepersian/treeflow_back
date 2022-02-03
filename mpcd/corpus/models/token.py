import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib import admin
from mpcd.dict.models import Entry
from .author import Author
from .bibliography import BibEntry
from .dependency import Dependency
from .morphological_annotation import MorphologicalAnnotation
from .pos import POS
from .text import Text


class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    text = models.ForeignKey(Text, on_delete=models.CASCADE, null=True, blank=True, related_name='token_text')
    transcription = models.CharField(max_length=50)
    transliteration = models.CharField(max_length=50, blank=True)
    lemma = models.ForeignKey(Entry, on_delete=models.CASCADE, null=True, blank=True, related_name='token_lemma')
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, null=True)
    morphological_annotation = models.ManyToManyField(
        MorphologicalAnnotation, blank=True, related_name='token_morphological_annotation')
    syntactic_annotation = models.ManyToManyField(Dependency, blank=True, related_name="token_syntactic_annotation")
    comment = models.TextField(blank=True)
    avestan = models.URLField(max_length=100, null=True, blank=True)
    previous = models.OneToOneField('self',
                                    related_name='token_previous',
                                    blank=True,
                                    null=True,
                                    on_delete=models.DO_NOTHING)

    history = HistoricalRecords()

    def ms_features(self):
        return "|\n".join([p.feature.name + '=' + p.feature_value.name for p in self.morphological_annotation.all()])

    def __str__(self):
        return '{}'.format(self.transcription)


class TokenAdmin(admin.ModelAdmin):
    raw_id_fields = ['lemma']
