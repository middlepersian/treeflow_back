from django.db import models
import uuid as uuid_lib
from simple_history.models import HistoricalRecords
from .comment import Comment
from .text import Text
from .section_type import SectionType
from .source import Source
from .token import Token


class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    text = models.ForeignKey(Text, on_delete=models.CASCADE, null=True, blank=True, related_name='section_text')
    number = models.FloatField(null=True, blank=True)
    identifier = models.CharField(max_length=100, blank=True, null=True, unique=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=3, blank=True)
    section_type = models.ForeignKey(SectionType, on_delete=models.CASCADE,
                                     related_name='section_section_type', null=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, related_name='section_source', null=True, blank=True)
    tokens = models.ManyToManyField(Token, related_name='section_tokens')
    previous = models.OneToOneField('self', on_delete=models.SET_NULL, null=True,
                                    blank=True, related_name='next')
    # this is the case if a section "paragraph" has a "chapter" container
    container = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,
                                  blank=True, related_name='section_container')
    meanings = models.ManyToManyField('dict.Meaning', related_name='section_meanings')

    history = HistoricalRecords()

    class Meta:
        ordering = ['number']

    def __str__(self) -> str:
        return '{}'.format(self.identifier)
