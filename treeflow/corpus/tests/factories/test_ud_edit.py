import pytest
from treeflow.corpus.models import Token, Dependency
from treeflow.corpus.tests.factories import TokenFactory, TextFactory

# write a test to create a new dependency between tokens

@pytest.mark.django_db
def test_create_dependency():
    """Test text factory"""
    text = TextFactory()

    # Create a sequence of tokens with known numbers
    token1 = TokenFactory(text=text, number=1.0)
    token2 = TokenFactory(text=text, number=2.0)
    token3 = TokenFactory(text=text, number=3.0)

    # Link tokens manually or by some setup logic
    token1.next = token2
    token2.previous = token1
    token2.next = token3
    token3.previous = token2
    token1.save()
    token2.save()
    token3.save()

    # Create a dependency between tokens
    dep = Dependency.objects.create(token=token1, head=token2)
    dep.save()

    # Check that the dependency was created
    assert dep.token == token1
    assert dep.head == token2
    assert dep.token.next == token2
    assert dep.rel == None
    assert dep.enhanced == False

    print(dep)