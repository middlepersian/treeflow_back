import factory
from treeflow.corpus.models import Facsimile


class FacsimileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Facsimile

    bib_entry = factory.SubFactory("treeflow.corpus.tests.factories.BibEntryFactory")
    codex = factory.SubFactory("treeflow.corpus.tests.factories.CodexFactory")