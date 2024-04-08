import uuid as uuid_lib
from django.db import models
from django.utils import timezone
from django.conf import settings
from treeflow.utils.normalize import strip_and_normalize


class POS(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    token = models.ForeignKey('Token', on_delete=models.CASCADE, null=True, blank=True, related_name='pos_token')
    pos = models.CharField(max_length=10, null=True, blank=True)
    #upos, xpos
    type = models.CharField(max_length=10, null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_pos')

    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='modified_pos',
        blank=True
    )
    
        
    def __str__(self):
        return '{} - {} - {}'.format(self.token, self.token.number, self.pos)
    class Meta:
        indexes = [models.Index(fields=['pos'])]

    def save(self, *args, **kwargs):
        # Normalize only the `normalized_field` before saving
        if self.pos:
            self.pos = strip_and_normalize('NFC', self.pos)
            # uppercase pos
            self.pos = self.pos.upper()

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
