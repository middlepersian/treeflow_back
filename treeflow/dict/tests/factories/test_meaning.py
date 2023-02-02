import pytest
from treeflow.dict.models import Meaning
from treeflow.dict.tests.factories import MeaningFactory


@pytest.mark.django_db
def test_meaning_factory():
    meaning = MeaningFactory()
    assert isinstance(meaning, Meaning)
    assert meaning.meaning is not None
    assert meaning.language is not None
    assert meaning.related_meanings is not None
