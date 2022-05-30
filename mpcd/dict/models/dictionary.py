import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords

class Dictionary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    source_languages = models.CharField(max_length=3, null=True, blank=True)
    slug = models.SlugField(max_length=10, unique=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'slug'], name='dictionary_name_slug'
            )
        ]

    def __str__(self):
        return self.name
