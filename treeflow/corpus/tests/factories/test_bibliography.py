import pytest
from treeflow.corpus.models import BibEntry
from treeflow.corpus.tests.factories import BibEntryFactory

@pytest.mark.django_db
def test_bib_entry_factory():
    bib_entry = BibEntryFactory()
    assert isinstance(bib_entry, BibEntry)
    assert bib_entry.key is not None
