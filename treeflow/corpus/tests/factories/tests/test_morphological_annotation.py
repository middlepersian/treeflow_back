import pytest
from treeflow.corpus.models import MorphologicalAnnotation
from treeflow.corpus.tests.factories import MorphologicalAnnotationFactory

@pytest.mark.django_db
def test_morphological_annotation_factory():
    ma1 = MorphologicalAnnotationFactory(feature='x1', feature_value='x2')
    ma2 = MorphologicalAnnotationFactory(feature='x1', feature_value='x3')
    ma3 = MorphologicalAnnotationFactory(feature='x1', feature_value='x2')
    ma4 = MorphologicalAnnotationFactory(feature='x1', feature_value='x3')

    assert MorphologicalAnnotation.objects.count() == 2
