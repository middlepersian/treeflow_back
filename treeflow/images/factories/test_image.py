import pytest
from treeflow.images.models import Image
from . import ImageFactory

@pytest.mark.django_db
def test_folio_factory():
    folio = ImageFactory()
    assert isinstance(folio, Image)
    assert folio.identifier is not None
    assert folio.number is not None
    assert folio.facsimile is not None
    previous = FolioFactory()
    folio.previous = previous
    assert isinstance(folio.previous, Folio)
