import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords



class CommentCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    category = models.CharField(max_length=1, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(self.category)
