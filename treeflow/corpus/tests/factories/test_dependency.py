import pytest
from treeflow.corpus.models import Dependency
from treeflow.corpus.tests.factories import DependencyFactory
'''
@pytest.mark.django_db
def test_dependency_factory():
    dependency = DependencyFactory()
    assert isinstance(dependency, Dependency)
    assert dependency.head is not None
    assert dependency.rel in ["nsubj", "dobj", "ccomp", "pobj", "iobj"]
    assert dependency.producer in [1, 2]
'''
