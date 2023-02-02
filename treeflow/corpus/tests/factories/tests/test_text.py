import pytest
from treeflow.corpus.models import Text
from treeflow.corpus.tests.factories import TextFactory
from treeflow.users.tests.factories import UserFactory


@pytest.mark.django_db
def test_text_factory():
    """Test text factory"""
    text = TextFactory()
    assert isinstance(text, Text)

    assert text.title
    assert text.stage
    assert text.text_sigle
    assert text.corpus

    # create a user and add it to the editors
    user = UserFactory()
    text.editors.add(user)
    assert text.editors.count() == 1