import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from treeflow.utils.normalize import strip_and_normalize

class POS(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    token = models.ForeignKey('Token', on_delete=models.CASCADE, null=True, blank=True, related_name='pos_token')
    pos = models.CharField(max_length=10, null=True, blank=True)
    #upos, xpos
    type = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()
    
        
    def __str__(self):
        return '{}'.format(self.pos)    

    class Meta:
        pass

    def save(self, *args, **kwargs):
        # Normalize only the `normalized_field` before saving
        if self.pos:
            self.pos = strip_and_normalize('NFC', self.pos)
            # uppercase pos
            self.pos = self.pos.upper()
        super().save(*args, **kwargs)
    