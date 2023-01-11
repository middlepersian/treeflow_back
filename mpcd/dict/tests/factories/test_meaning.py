import pytest
from mpcd.dict.models import Meaning
from mpcd.dict.tests.factories import MeaningFactory


@pytest.mark.django_db
def test_meaning_factory():
    meaning = MeaningFactory()
    assert isinstance(meaning, Meaning)
    assert meaning.meaning is not None
    assert meaning.language is not None
    assert meaning.related_meanings is not None
