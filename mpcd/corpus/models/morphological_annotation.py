from dataclasses import fields
import uuid as uuid_lib
from django.db import models
from .feature import Feature
from .feature_value import FeatureValue


class MorphologicalAnnotation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    feature = models.CharField(max_length=10, null=True, blank=True)
    feature_value = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['feature', 'feature_value'], name='feature_featurevalue'
            )
        ]

    def __str__(self):
        return '{} {}'.format(self.feature, self.feature_value)
