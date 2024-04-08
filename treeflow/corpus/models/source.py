import uuid as uuid_lib
from django.db import models
from django.conf import settings
from django.utils import timezone
from .bibliography import BibEntry
from treeflow.utils.normalize import strip_and_normalize


class Source(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    # codex, facsimile, edition, etc
    type = models.CharField(max_length=10, null=True, blank=True)

    identifier = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    references = models.ManyToManyField(BibEntry, blank=True, related_name='source_references')

    # a 'source' might have another sources as a source
    sources = models.ManyToManyField('self',blank=True, related_name='source_sources')

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_sources')

    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='modified_sources',
        blank=True
    )


    class Meta:
        ordering = ['identifier']
        constraints = [

            models.UniqueConstraint(
                fields=['type', 'identifier'], name='source_type_identifier'
            )
        ]


    def __str__(self):
        return '{}'.format(self.identifier)
    
    def save(self, *args, **kwargs):
        #normalize type
        if self.type:
            self.type = strip_and_normalize('NFC', self.type)
            #lowercase type
            self.type = self.type.lower()
        if self.identifier:    
            #normalize identifier
            self.identifier = strip_and_normalize('NFC', self.identifier)
        if self.description:
            #normalize description
            self.description = strip_and_normalize('NFC', self.description)


        is_new = self._state.adding
        user = kwargs.pop('user', None)  
        # Handle the user for created_by and modified_by
        if is_new and user:
            self.created_by = user
        elif not is_new:
            self.modified_at = timezone.now()
            self.modified_by = user

            # Ensure 'modified_at' and 'modified_by' are included in 'update_fields'
            if 'update_fields' in kwargs:
                update_fields = set(kwargs['update_fields'])
                update_fields.update({'modified_at', 'modified_by'})
                kwargs['update_fields'] = list(update_fields)

        super().save(*args, **kwargs)
