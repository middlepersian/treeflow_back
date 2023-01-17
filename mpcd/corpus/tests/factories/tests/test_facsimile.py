import pytest
from mpcd.corpus.models import Facsimile
from mpcd.corpus.tests.factories import FacsimileFactory, BibEntryFactory

@pytest.mark.django_db
def test_facsimile_factory():

    bib_entry = BibEntryFactory()
    facsimile = FacsimileFactory(bib_entry=bib_entry)
    assert isinstance(facsimile, Facsimile)

