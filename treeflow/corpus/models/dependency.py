import uuid as uuid_lib
from django.db import models
from django.conf import settings
from django.utils import timezone
from treeflow.utils.normalize import strip_and_normalize

class Dependency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    token = models.ForeignKey("Token", on_delete=models.CASCADE, related_name='dependency_token')
    head = models.ForeignKey("Token", on_delete=models.SET_NULL, related_name='dependency_head', null=True, blank=True)
    head_number = models.FloatField(null=True, blank=True)
    rel = models.CharField(max_length=25, null=True, blank=True)
    #enahnced in case of deps (default: False)
    enhanced = models.BooleanField(default=False)
    # producer values: manual(1), computational(2). see schemas/dependency_enum.py
    producer = models.SmallIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_dependencies')

    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='modified_dependencies',
        blank=True
    )


    def __str__(self):
        return '{} {}'.format(str(self.head), self.rel)


    class Meta:
        pass

    
    def save(self, *args, **kwargs):
        # Normalize only the `normalized_field` before saving
        if self.rel:
            self.rel = strip_and_normalize('NFC', self.rel)
            # lowercase the rel
            self.rel = self.rel.lower()
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