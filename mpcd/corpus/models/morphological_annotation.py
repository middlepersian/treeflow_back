import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords


class MorphologicalAnnotation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    feature = models.CharField(max_length=10, null=True, blank=True)
    feature_value = models.CharField(max_length=10, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['feature', 'feature_value'], name='feature_featurevalue'
            )
        ]

    def __str__(self):
        return '{} {}'.format(self.feature, self.feature_value)
