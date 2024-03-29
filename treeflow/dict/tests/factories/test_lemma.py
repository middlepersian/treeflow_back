import pytest
from treeflow.dict.models import Lemma
from treeflow.dict.tests.factories import LemmaFactory

@pytest.mark.django_db
def test_lemma_factory():
    lemma = LemmaFactory()
    assert isinstance(lemma, Lemma)
    assert lemma.word is not None
    assert lemma.language is not None
    assert lemma.related_meanings is not None