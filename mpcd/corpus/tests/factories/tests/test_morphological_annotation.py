import pytest
from mpcd.corpus.models import MorphologicalAnnotation
from mpcd.corpus.tests.factories import MorphologicalAnnotationFactory

@pytest.mark.django_db
def test_morphological_annotation_factory():
    annotation = MorphologicalAnnotationFactory()
    assert isinstance(annotation, MorphologicalAnnotation)
    assert annotation.feature is not None
    assert annotation.feature_value is not None
