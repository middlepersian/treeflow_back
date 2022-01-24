from .author import Author
from django.db import models
import uuid as uuid_lib


class Resource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    authors = models.ManyToManyField(Author, blank=True, related_name='resource_authors')
    description = models.TextField(blank=True, null=True)
    project = models.TextField(blank=True, null=True)
    reference = models.URLField(blank=True, null=True)
