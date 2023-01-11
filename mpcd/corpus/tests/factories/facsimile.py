import factory
from faker import Faker
from mpcd.corpus.models import Facsimile

class FacsimileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Facsimile
    
    bib_entry = factory.SubFactory("mpcd.tests.factories.BibEntryFactory")
    codex_part = factory.SubFactory("mpcd.tests.factories.CodexPartFactory")
