import uuid as uuid_lib
from django.db import models
from django.conf import settings
from django.utils import timezone
from treeflow.utils.normalize import strip_and_normalize

class Feature(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    token = models.ForeignKey('Token', on_delete=models.CASCADE, null=True, blank=True, related_name='feature_token')
    pos = models.ForeignKey('POS', on_delete=models.CASCADE, null=True, blank=True, related_name='feature_pos')
    feature = models.CharField(max_length=10, null=True, blank=True)
    feature_value = models.CharField(max_length=10, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_features')

    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='modified_features',
        blank=True
    )
    
    def __str__(self):
        return '{} {}'.format(self.feature, self.feature_value)


    class Meta:
        indexes = [models.Index(fields=['feature', 'feature_value'])]
    
    def save(self, *args, **kwargs):
        # Normalize only the `normalized_field` before saving
        if self.feature:
            self.feature = strip_and_normalize('NFC', self.feature)
        if self.feature_value:
            self.feature_value = strip_and_normalize('NFC', self.feature_value)

        is_new = self._state.adding
        logger.debug('kwargs before pop: {}'.format(kwargs))
        user = kwargs.pop('user', None)  
        logger.debug('kwargs after pop: {}'.format(kwargs))  
        # Handle the user for created_by and modified_by
        if is_new and user:
            self.created_by = user
            logger.info('Setting created_by: {}'.format(self.created_by))
        elif not is_new:
            self.modified_at = timezone.now()
            self.modified_by = user
            logger.info('Setting modified_by: {}'.format(self.modified_by))

            # Ensure 'modified_at' and 'modified_by' are included in 'update_fields'
            if 'update_fields' in kwargs:
                update_fields = set(kwargs['update_fields'])
                update_fields.update({'modified_at', 'modified_by'})
                kwargs['update_fields'] = list(update_fields)

        super().save(*args, **kwargs)
