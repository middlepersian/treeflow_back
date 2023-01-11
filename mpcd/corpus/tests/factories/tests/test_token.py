import pytest
from mpcd.corpus.models import Token
from mpcd.corpus.tests.factories import TokenFactory


@pytest.mark.django_db
def test_token_factory():
    token = TokenFactory()
    assert isinstance(token, Token)
    '''
    assert token.number is not None
    assert isinstance(token.root, bool)
    assert isinstance(token.word_token, bool)
    assert isinstance(token.visible, bool)
    assert token.text is not None
    assert token.sentence is not None
    assert token.language is not None
    assert token.transcription is not None
    assert token.transliteration is not None
    assert token.pos is not None
    assert token.avestan is not None
    assert token.line is not None
    assert token.previous is not None
    assert token.gloss is not None
    assert token.lemmas is not None
    assert token.meanings is not None
    assert token.morphological_annotation is not None
    assert token.syntactic_annotation is not None
    '''
