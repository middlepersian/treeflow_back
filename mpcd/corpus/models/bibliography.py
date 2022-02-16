import uuid as uuid_lib
from django.db import models
from .author import Author


class BibEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    authors = models.ManyToManyField(Author, related_name="bib_entry_authors", blank=True)
    title = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField(null=True, blank=True)

    url = models.URLField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'year'], name='title_year_unique'
            )
        ]

    def get_authors(self):
        return "|\n".join([p.last_name + ' , ' + p.name for p in self.authors.all()])

    def __str__(self):
        return '{} {}'.format(self.title, self.year)
