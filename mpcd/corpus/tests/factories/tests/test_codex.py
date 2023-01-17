import pytest
from mpcd.corpus.tests.factories import CodexFactory
from mpcd.corpus.models import Codex

@pytest.mark.django_db
def test_create_codex():
    # Create a Codex object
    codex = CodexFactory(sigle="TRD")
    codex_1 = CodexFactory(sigle="TRD")
    assert Codex.objects.count() == 1

    