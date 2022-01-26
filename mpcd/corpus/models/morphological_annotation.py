from dataclasses import fields
import uuid as uuid_lib
from django.db import models
from .feature import Feature
from .feature_value import FeatureValue


class MorphologicalAnnotation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='morphological_annotation_feature')
    feature_value = models.ForeignKey(FeatureValue, on_delete=models.CASCADE, null=True,
                                      blank=True, related_name='morphological_annotation_feature_value')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['feature', 'feature_value'], name='feature_featurevalue'
            )
        ]

    def __str__(self):
        return '{} {}'.format(self.feature, self.feature_value)
