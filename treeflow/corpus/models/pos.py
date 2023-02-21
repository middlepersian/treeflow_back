import uuid as uuid_lib
from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords

class POS(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    token = models.ForeignKey('Token', on_delete=models.CASCADE, null=True, blank=True, related_name='pos_token')
    pos = models.CharField(max_length=10, null=True, blank=True)
    #upos, xpos
    type = models.CharField(max_length=10, null=True, blank=True)
    history = HistoricalRecords()
    
        
    def __str__(self):
        return '{}'.format(self.pos)    

    class Meta:
        unique_together = ('token', 'pos')
        indexes = [
            models.Index(fields=['token', 'pos', 'type']),
        ]