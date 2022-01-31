import imp
from django.db import models
import uuid as uuid_lib
from simple_history.models import HistoricalRecords
from .text import Text
from .section_type import SectionType


class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    text = models.ForeignKey(Text, on_delete=models.CASCADE, null=True, blank=True, related_name='section_text')
    section_type = models.ForeignKey(SectionType, on_delete=models.CASCADE, related_name='section_section_type')
    identifier = models.CharField(max_length=100, blank=True, null=True)
    tokens = models.ManyToManyField('Token', related_name='section_tokens')
    previous = models.OneToOneField('self', on_delete=models.DO_NOTHING, null=True,
                                    blank=True, related_name='section_previous')

    history = HistoricalRecords()

    def __str__(self) -> str:
        return '{}'.format(self.identifier)
