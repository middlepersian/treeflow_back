import pytest
from treeflow.corpus.models import Section
from treeflow.corpus.tests.factories import SectionFactory
from treeflow.corpus.models import Section, Text

import pytest
from treeflow.corpus.models import Section, Text
from django.db import transaction

@pytest.fixture
def test_text(db):
    return Text.objects.create(title="Test Text")

@pytest.fixture
def initial_sections(db, test_text):
    sections = [
        Section.objects.create(text=test_text, number=1.0),
        Section.objects.create(text=test_text, number=2.0),
        Section.objects.create(text=test_text, number=3.0)
    ]
    # Link the sections
    for i in range(len(sections) - 1):
        sections[i].next = sections[i + 1]
        sections[i + 1].previous = sections[i]
        sections[i].save()
        sections[i + 1].save()
    return sections

@pytest.mark.django_db
def test_insert_section_before(test_text, initial_sections):
    middle_section = initial_sections[1]
    new_section_data = {'title': 'New Section', 'text': test_text}

    with transaction.atomic():
        new_section = Section.insert_before(middle_section.id, new_section_data)
        #refresh the db
        middle_section.refresh_from_db()
        new_section.refresh_from_db()


    assert new_section is not None
    assert new_section.number < middle_section.number
    assert new_section.next == middle_section
    assert new_section.previous == initial_sections[0]
    assert middle_section.previous == new_section


@pytest.mark.django_db
def test_insert_section_after(test_text, initial_sections):
    middle_section = initial_sections[1]
    new_section_data = {'title': 'New Section', 'text': test_text}

    with transaction.atomic():
        new_section = Section.insert_after(middle_section.id, new_section_data)
        #refresh the db
        middle_section.refresh_from_db()
        new_section.refresh_from_db()

    assert new_section is not None
    assert new_section.number > middle_section.number
    assert new_section.previous == middle_section
    assert new_section.next == initial_sections[2]
    assert middle_section.next == new_section