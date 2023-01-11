import pytest
from mpcd.corpus.models import Facsimile
from mpcd.corpus.tests.factories import FacsimileFactory

@pytest.mark.django_db
def test_facsimile_factory():
    facsimile = FacsimileFactory()
    assert isinstance(facsimile, Facsimile)
    assert facsimile.bib_entry is not None
    assert facsimile.codex_part is not None
