import pytest
from mpcd.corpus.models import Token
from mpcd.corpus.tests.factories import TokenFactory


@pytest.mark.django_db
def test_token_factory():
    """Test token factory"""
    token = TokenFactory()
    assert isinstance(token, Token)

    assert token.number
    assert token.root == False
    assert token.word_token
    assert token.visible
    assert token.text
    assert token.sentence
    assert token.language
    assert token.transcription
    assert token.transliteration
    assert token.pos
    assert token.avestan
    assert token.gloss
    assert token.lemmas
    assert token.meanings
    assert token.morphological_annotation
    assert token.syntactic_annotation
