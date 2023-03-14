import uuid as uuid_lib
from django.contrib.postgres.fields import ArrayField
from django.db import models
from simple_history.models import HistoricalRecords
from django.conf import settings
from treeflow.utils.normalize import strip_and_normalize



class Text(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    corpus = models.ForeignKey('Corpus', on_delete=models.CASCADE, null=True, blank=True, related_name='text_corpus')
    title = models.CharField(max_length=100, null=True, blank=True)
    identifier = models.CharField(max_length=20, null=True, blank=True)
    language = ArrayField(models.CharField(max_length=3), blank=True, null=True)
    #e.g. sigle
    series = models.CharField(max_length=20, null=True,blank=True)
    # e.g. genre
    label = models.CharField(max_length=20, null=True, blank=True)
    stage = models.CharField(max_length=10, blank=True)
    
    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="text_editors")
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="text_collaborators")
   
    # a any source that should be documented in Zotero
    sources = models.ManyToManyField('Source', blank=True, related_name='text_sources')
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']
        constraints = [
            models.UniqueConstraint(
                fields=['corpus', 'identifier'], name='text_corpus_identifier'
            )
        ]
    def save(self, *args, **kwargs):
            
        if self.title:    
            #normalize title
            self.title = strip_and_normalize('NFC', self.title)

        if self.identifier:
            #normalize identifier
            self.identifier = strip_and_normalize('NFC', self.identifier)

        if self.series:
            #normalize series
            self.series = strip_and_normalize('NFC', self.series)

        if self.label:
            #normalize label
            self.label = strip_and_normalize('NFC', self.label)

        if self.stage:
            #normalize stage
            self.stage = strip_and_normalize('NFC', self.stage)

        if self.language:
            self.language = [l.strip().lower() for l in self.language]
        #save
        super().save(*args, **kwargs)