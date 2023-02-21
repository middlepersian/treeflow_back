from django.db import models
import uuid as uuid_lib
from simple_history.models import HistoricalRecords
from django.conf import settings


class Corpus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'slug'], name='corpus_name_slug'
            )
        ]

    def __str__(self):
        return self.slug
