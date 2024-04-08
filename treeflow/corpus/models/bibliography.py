import uuid as uuid_lib
from django.db import models
from django.conf import settings
from django.utils import timezone
from treeflow.utils.normalize import strip_and_normalize

class BibEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    # Zotero key
    key = models.CharField(blank=True, null=True, max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_bib_entries')

    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='modified_bib_entries',
        blank=True
    )

    def __str__(self):
        return '{}'.format(self.key)

    def save(self, *args, **kwargs):
        if self.key:  # Ensuring that key is not None before stripping and lowering
            self.key = strip_and_normalize('NFC', self.key)
            self.key = self.key.lower()

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