
from django.db import models
from .author import Author

class BibEntry(models.Model):
    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    url = models.URLField(blank=True, null=True)

    def get_authors(self):
        return "|\n".join([p.last_name + ' , ' + p.name for p in self.authors.all()])

    def __str__(self):
        return '{} {}'.format(self.title, self.year)
