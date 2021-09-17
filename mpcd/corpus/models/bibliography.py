from typing import Mapping

from django.db import models
from .author import Author


class BibEntry(models.Model):
    author = models.ManyToManyField(Author)
    title = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    url = models.URLField(blank=True, null=True)
