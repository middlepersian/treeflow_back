from django.db import models
import uuid as uuid_lib
from treeflow.utils.normalize import strip_and_normalize

class Corpus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'slug'], name='corpus_name_slug'
            )
        ]

    def __str__(self):
        return self.slug
    

    def save(self, *args, **kwargs):
        # Normalize only the `normalized_field` before saving
        self.name = strip_and_normalize('NFC', self.name)
        self.slug = strip_and_normalize('NFC', self.slug)
        super().save(*args, **kwargs)
