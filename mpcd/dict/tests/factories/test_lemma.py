import pytest
from mpcd.dict.models import Lemma
from mpcd.dict.tests.factories import LemmaFactory

@pytest.mark.django_db
def test_lemma_factory():
    lemma = LemmaFactory()
    assert isinstance(lemma, Lemma)
    assert lemma.word is not None
    assert lemma.language is not None
    assert lemma.related_meanings is not None