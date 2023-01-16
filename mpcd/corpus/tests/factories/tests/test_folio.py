import pytest
from mpcd.corpus.models import Folio
from mpcd.corpus.tests.factories import FolioFactory

@pytest.mark.django_db
def test_folio_factory():
    folio = FolioFactory()
    assert isinstance(folio, Folio)
    assert folio.identifier is not None
    assert folio.number is not None
    assert folio.facsimile is not None
    previous = FolioFactory()
    folio.previous = previous
    assert isinstance(folio.previous, Folio)
