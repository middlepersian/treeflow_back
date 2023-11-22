import pytest
from treeflow.corpus.models import Section
from treeflow.corpus.tests.factories import SectionFactory


@pytest.mark.django_db
def test_section_factory():
    section = SectionFactory()
    assert isinstance(section, Section)

    # Add assertions for all relevant properties of the Section model
    assert section.text
    assert section.identifier
    assert section.type
    assert section.title
    assert section.language
    assert section.source
    assert section.tokens

    # Test linking to a previous section
    previous_section = SectionFactory()
    section.previous = previous_section
    assert section.previous == previous_section


@pytest.mark.django_db
def test_insert_before():
    # Create a sequence of sections
    first_section = SectionFactory(number=1.0)
    second_section = SectionFactory(number=2.0, previous=first_section)

    # Prepare data for the new section
    new_section_data = {
        'text': second_section.text,  # Assuming the new section belongs to the same text
        'identifier': 'new_section_identifier',
        'type': first_section.type,
        'title': 'New Section Title',
        'language': 'en',
        'source': second_section.source,  # Assuming the same source as the second section
    }
    
    new_section = Section.insert_before(second_section.id, new_section_data)

    # Reload sections from the database
    first_section.refresh_from_db()
    second_section.refresh_from_db()

    # Assert conditions after insertion
    assert new_section.previous == first_section
    assert second_section.previous == new_section



@pytest.mark.django_db
def test_insert_after():
    # Create a sequence of sections
    first_section = SectionFactory(number=1.0)
    second_section = SectionFactory(number=2.0, previous=first_section)

    # Prepare data for the new section
    new_section_data = {
        'text': second_section.text,  # Assuming the new section belongs to the same text
        'identifier': 'new_section_identifier',
        'type': first_section.type,
        'title': 'New Section Title',
        'language': 'en',
        'source': second_section.source,  # Assuming the same source as the second section
    }

    new_section = Section.insert_after(first_section.id, new_section_data)

    # Reload sections from the database
    first_section.refresh_from_db()
    second_section.refresh_from_db()

    # Assert conditions after insertion
    assert new_section.previous == first_section
    assert second_section.previous == new_section
