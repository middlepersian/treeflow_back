import pytest
from treeflow.images.models import Facsimile
from . import FacsimileFactory
from treeflow.corpus.tests.factories import BibEntryFactory

@pytest.mark.django_db
def test_facsimile_factory():

    bib_entry = BibEntryFactory()
    facsimile = FacsimileFactory(bib_entry=bib_entry)
    assert isinstance(facsimile, Facsimile)