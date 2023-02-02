import pytest
from treeflow.corpus.models import SectionType
from treeflow.corpus.tests.factories import SectionTypeFactory

@pytest.mark.django_db
def test_section_type_factory():
    section_type = SectionTypeFactory()
    assert isinstance(section_type, SectionType)
    assert section_type.identifier is not None
