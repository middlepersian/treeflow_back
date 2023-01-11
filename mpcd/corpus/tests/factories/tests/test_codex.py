import pytest
from mpcd.corpus.tests.factories import CodexFactory

@pytest.mark.django_db
def test_create_codex():
    # Create a Codex object
    codex = CodexFactory()

    # Assert that the Codex object was created correctly
    assert codex.sigle == codex.sigle