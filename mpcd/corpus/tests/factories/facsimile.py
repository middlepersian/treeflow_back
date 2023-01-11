import factory
from mpcd.corpus.models import Facsimile

class FacsimileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Facsimile
    
    bib_entry = factory.SubFactory("mpcd.corpus.tests.factories.BibEntryFactory")
    codex_part = factory.SubFactory("mpcd.corpus.tests.factories.CodexPartFactory")
