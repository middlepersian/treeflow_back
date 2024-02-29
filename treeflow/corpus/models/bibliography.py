import uuid as uuid_lib
from django.db import models


class BibEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    # Zotero key
    key = models.CharField(blank=True, null=True, max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.key)

    def save(self, *args, **kwargs):
        # Normalize only the `normalized_field` before saving
        self.key = self.key.strip().lower()
        super().save(*args, **kwargs)
