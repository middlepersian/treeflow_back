import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from treeflow.utils.normalize import strip_and_normalize

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
        pass
    
    def save(self, *args, **kwargs):
        # Normalize only the `normalized_field` before saving
        if self.feature:
            self.feature = strip_and_normalize('NFC', self.feature)
        if self.feature_value:
            self.feature_value = strip_and_normalize('NFC', self.feature_value)
        super().save(*args, **kwargs)
    