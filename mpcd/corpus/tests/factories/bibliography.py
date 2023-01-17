import factory
from mpcd.corpus.models import BibEntry

class BibEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BibEntry
        django_get_or_create = ('key',)

    key = factory.Faker("word")