import uuid as uuid_lib
from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords


class Feature(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    token = models.ForeignKey('Token', on_delete=models.CASCADE, null=True, blank=True, related_name='feature_token')
    pos = models.ForeignKey('POS', on_delete=models.CASCADE, null=True, blank=True, related_name='feature_pos')
    feature = models.CharField(max_length=10, null=True, blank=True)
    feature_value = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()
    
    def __str__(self):
        return '{} {}'.format(self.feature, self.feature_value)


    class Meta:
        indexes = [
            models.Index(fields=['token', 'pos', 'feature', 'feature_value']),
        ]