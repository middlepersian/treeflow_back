
import uuid as uuid_lib
from django.db import models


class FeatureValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    # e.g. 'Prs'
    identifier = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return '{}'.format(self.name)
