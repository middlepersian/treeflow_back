import uuid as uuid_lib
from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords


class Image(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    identifier = models.CharField(max_length=100)
    page = models.CharField(max_length=100, null=True, blank=True)

    number = models.FloatField(null=True, blank=True)
    # In some cases, as in MK, images can have a source directly a "Codex" or a "Facsimile"
    source = models.ForeignKey('corpus.Source', on_delete=models.CASCADE, null=True,
                                  blank=True, related_name='image_source')
    previous = models.OneToOneField('self',
                                    related_name='next',
                                    blank=True,
                                    null=True,
                                    on_delete=models.DO_NOTHING)

    # lines
    sections = models.ManyToManyField('corpus.Section', related_name='image_sections', through='ImageSection')                                
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['identifier', 'number']
        constraints = [
            models.UniqueConstraint(
                fields=['source', 'identifier'], name='image_source_identifier'
            )
        ]
        indexes= [
            models.Index(fields=['source', 'identifier', 'number', 'previous']),
        ]

    def __str__(self):
        return '{}'.format(self.identifier)


class ImageSection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    image = models.ForeignKey('Image', on_delete=models.CASCADE)
    section = models.ForeignKey('corpus.Section', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()


    class Meta:
        ordering = ['image', 'section']
        constraints = [
            models.UniqueConstraint(
                fields=['image', 'section'], name='image_section_image_section'
            )
        ]
        indexes = [
            models.Index(fields=['image', 'section']),
        ]

    def __str__(self):
        return '{} - {}'.format(self.image, self.section)