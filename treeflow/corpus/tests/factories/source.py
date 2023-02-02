import factory
from treeflow.corpus.models import Source

class SourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Source

    identifier = factory.Faker("pystr", min_chars=1, max_chars=15)
    bib_entry = factory.SubFactory("treeflow.corpus.tests.factories.BibEntryFactory")
    description = factory.Faker("text")
