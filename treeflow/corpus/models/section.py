from django.db import models
from django.conf import settings
import uuid as uuid_lib
from simple_history.models import HistoricalRecords



class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    text = models.ForeignKey('Text', on_delete=models.CASCADE, null=True, blank=True, related_name='section_text')
    number = models.FloatField(null=True, blank=True)
    identifier = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=25, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=3, blank=True)
    source = models.ForeignKey('Source', on_delete=models.SET_NULL, related_name='section_source', null=True, blank=True)
    tokens = models.ManyToManyField('Token', related_name='section_tokens', through='SectionToken')
    previous = models.OneToOneField('self', on_delete=models.SET_NULL, null=True,
                                    blank=True, related_name='next')
    # this is the case if a section "paragraph" has a "chapter" container
    container = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,
                                  blank=True, related_name='section_container')
    meanings = models.ManyToManyField('dict.Meaning', related_name='section_meanings')
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()


    class Meta:
        ordering = ['created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['text', 'identifier'], name='section_text_identifier' )
        ]
        indexes = [models.Index(fields=['text', 'number', 'identifier', 'previous','type', 'container']),
                models.Index(fields=['text']),
                models.Index(fields=['number']),
                models.Index(fields=['identifier']),
                models.Index(fields=['previous']),
                models.Index(fields=['container']),
                models.Index(fields=['type']),
                models.Index(fields=['created_at'])]

    def __str__(self) -> str:
        return '{}'.format(self.identifier)



class SectionToken(models.Model):
    section = models.ForeignKey('Section', on_delete=models.CASCADE)
    token = models.ForeignKey('Token', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['section']),
            models.Index(fields=['token']),
            models.Index(fields=['section', 'token']),
        ]

    def __str__(self):
        return 'SectionToken {}:{}'.format(self.section_id, self.token_id)
    
