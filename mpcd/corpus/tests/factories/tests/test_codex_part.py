from mpcd.corpus.tests.factories import CodexPartFactory
from mpcd.corpus.models import CodexPart
import pytest

@pytest.mark.django_db
def test_codex_part_factory():
    codex_part = CodexPartFactory()
    assert isinstance(codex_part, CodexPart)
    assert codex_part.slug is not None
    assert codex_part.codex is not None
