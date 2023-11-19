import pytest
from django.core.exceptions import ObjectDoesNotExist
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


@pytest.mark.django_db
def test_insert_section_at_beginning(test_text, initial_sections):
    first_section = initial_sections[0]
    new_section_data = {'title': 'New Section', 'text': test_text}

    with transaction.atomic():
        new_section = Section.insert_before(first_section.id, new_section_data)
        #refresh the db
        first_section.refresh_from_db()
        new_section.refresh_from_db()

    assert new_section is not None
    assert new_section.number < first_section.number
    assert new_section.next == first_section
    assert new_section.previous is None
    assert first_section.previous == new_section

@pytest.mark.django_db
def test_insert_section_at_end(test_text, initial_sections):
    last_section = initial_sections[-1]
    new_section_data = {'title': 'New Section', 'text': test_text}

    with transaction.atomic():
        new_section = Section.insert_after(last_section.id, new_section_data)
        #refresh the db
        last_section.refresh_from_db()
        new_section.refresh_from_db()

    assert new_section is not None
    assert new_section.number > last_section.number
    assert new_section.previous == last_section
    try:
        new_section_next = new_section.next
    except ObjectDoesNotExist:
        new_section_next = None
    assert new_section_next is None
    assert last_section.next == new_section


@pytest.mark.django_db
def test_insert_multiple_sections(test_text, initial_sections):
    first_section = initial_sections[0]
    new_section_data1 = {'title': 'New Section 1', 'text': test_text}
    new_section_data2 = {'title': 'New Section 2', 'text': test_text}

    with transaction.atomic():
        new_section1 = Section.insert_after(first_section.id, new_section_data1)
        new_section2 = Section.insert_after(new_section1.id, new_section_data2)
        #refresh the db
        first_section.refresh_from_db()
        new_section1.refresh_from_db()
        new_section2.refresh_from_db()

    assert new_section1.previous == first_section
    assert new_section1.next == new_section2
    assert new_section2.previous == new_section1
    assert first_section.next == new_section1    

@pytest.mark.django_db
def test_insert_section_after_section_with_next(test_text, initial_sections):
    first_section = initial_sections[0]
    second_section = initial_sections[1]
    new_section_data = {'title': 'New Section', 'text': test_text}

    with transaction.atomic():
        # Insert a new section after the first section
        new_section1 = Section.insert_after(first_section.id, new_section_data)
        # Refresh the db
        first_section.refresh_from_db()
        new_section1.refresh_from_db()

    assert new_section1.previous == first_section
    assert first_section.next == new_section1

    with transaction.atomic():
        # Try to insert another new section after the first section
        new_section2 = Section.insert_after(first_section.id, new_section_data)
        # Refresh the db
        first_section.refresh_from_db()
        new_section2.refresh_from_db()

    assert new_section2.previous == first_section
    assert new_section2.next == new_section1
    assert first_section.next == new_section2
    assert new_section1.previous == new_section2    