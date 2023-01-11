import pytest
from mpcd.corpus.models import Section
from mpcd.corpus.tests.factories import SectionFactory


@pytest.mark.django_db
def test_section_factory():
    section = SectionFactory()
    assert isinstance(section, Section)

    #assert section.number is not None
    #assert section.identifier is not None
    #assert section.text is not None
    #assert section.section_type is not None
    #assert section.source is not None
    #assert section.tokens is not None
    #assert section.previous is not None
    #assert section.container is not None
