import uuid as uuid_lib
from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from treeflow.corpus.enums.deprel import Deprel

class Dependency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    token = models.ForeignKey("Token", on_delete=models.CASCADE, related_name='dependency_token')
    head = models.ForeignKey("Token", on_delete=models.SET_NULL, related_name='dependency_head', null=True, blank=True)
    head_number = models.FloatField(null=True, blank=True)
    rel = models.CharField(max_length=25, null=True, blank=True)
    # producer values: manual(1), computational(2). see schemas/dependency_enum.py
    producer = models.SmallIntegerField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{} {}'.format(str(self.head), self.rel)


    class Meta:
        indexes = [
            models.Index(fields=['token', 'head', 'rel']),
        ]