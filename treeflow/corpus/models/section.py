from django.db import models
import uuid as uuid_lib
from simple_history.models import HistoricalRecords
from treeflow.utils.normalize import strip_and_normalize


class Section(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid_lib.uuid4, editable=False)
    text = models.ForeignKey('Text', on_delete=models.CASCADE,
                             null=True, blank=True, related_name='section_text')
    number = models.FloatField(null=True, blank=True)
    identifier = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=25, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=3, blank=True)
    source = models.ForeignKey('Source', on_delete=models.SET_NULL,
                               related_name='section_source', null=True, blank=True)
    tokens = models.ManyToManyField('Token', related_name='section_tokens', through='SectionToken')
    previous = models.OneToOneField('self', on_delete=models.SET_NULL, null=True,
                                    blank=True, related_name='next')
    # this is the case if a section "paragraph" has a "chapter" container
    container = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,
                                  blank=True, related_name='section_container')

    senses = models.ManyToManyField(
        'dict.Sense', related_name='section_senses')
            
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['number']
        constraints = [
            models.UniqueConstraint(
                fields=['text', 'identifier'], name='section_text_identifier')
        ]
        indexes = [models.Index(fields=['text', 'type']),
                   models.Index(fields=['type']),
                   ]

    def __str__(self) -> str:
        return '{} - {} '.format(self.type, self.identifier)

    @property
    def has_Enhanced(self) -> bool:
        return self.tokens.filter(dependency_token__enhanced=True).exists() 

    def save(self, *args, **kwargs):
        # Normalize only the `normalized_field` before saving
        if self.identifier:
            # normalize identifier
            self.identifier = strip_and_normalize('NFC', self.identifier)
        if self.type:
            # normalize type
            self.type = strip_and_normalize('NFC', self.type)
        if self.title:
            # process title
            self.title = strip_and_normalize('NFC', self.title)
        if self.language:
            # process language
            self.language = self.language.strip().lower()
        super().save(*args, **kwargs)


class SectionToken(models.Model):
    section = models.ForeignKey('Section', on_delete=models.CASCADE)
    token = models.ForeignKey('Token', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['section', 'token']),
            models.Index(fields=['token']),
            models.Index(fields=['section']),
        ]
        ordering = ['section', 'token']

    def __str__(self):
        return 'SectionToken {}:{}'.format(self.section_id, self.token_id)
