import factory
from mpcd.corpus.models import BibEntry

class BibEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BibEntry

    key = factory.Faker("word")