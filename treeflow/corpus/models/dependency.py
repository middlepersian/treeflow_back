import uuid as uuid_lib
from django.db import models
from treeflow.utils.normalize import strip_and_normalize

class Dependency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    token = models.ForeignKey("Token", on_delete=models.CASCADE, related_name='dependency_token')
    head = models.ForeignKey("Token", on_delete=models.SET_NULL, related_name='dependency_head', null=True, blank=True)
    head_number = models.FloatField(null=True, blank=True)
    rel = models.CharField(max_length=25, null=True, blank=True)
    #enahnced in case of deps (default: False)
    enhanced = models.BooleanField(default=False)
    # producer values: manual(1), computational(2). see schemas/dependency_enum.py
    producer = models.SmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


        
    def __str__(self):
        return '{} {}'.format(str(self.head), self.rel)


    class Meta:
        pass

    
    def save(self, *args, **kwargs):
        # Normalize only the `normalized_field` before saving
        if self.rel:
            self.rel = strip_and_normalize('NFC', self.rel)
            # lowercase the rel
            self.rel = self.rel.lower()
        super().save(*args, **kwargs)
    