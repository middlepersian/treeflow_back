import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords


class Dependency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)

    head = models.ForeignKey("Token", on_delete=models.SET_NULL, related_name='dependency_head', null=True, blank=True)
    head_number = models.FloatField(null=True, blank=True)
    rel = models.CharField(max_length=25)
    # producer values: manual(1), computational(2). see schemas/dependency_enum.py
    producer = models.SmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()


    def __str__(self):
        return '{} {}'.format(str(self.head), self.rel)

