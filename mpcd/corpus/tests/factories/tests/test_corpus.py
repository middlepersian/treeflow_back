import pytest
from mpcd.corpus.models import Corpus
from mpcd.corpus.tests.factories import CorpusFactory

@pytest.mark.django_db
def test_corpus_factory():
    corpus = CorpusFactory()
    assert isinstance(corpus, Corpus)
    assert corpus.name is not None
    assert corpus.slug is not None
