import pytest
from treeflow.corpus.models import PostFeature
from treeflow.corpus.tests.factories import PostFeatureFactory

@pytest.mark.django_db
def test_morphological_annotation_factory():
    ma1 = PostFeatureFactory(feature='x1', feature_value='x2')
    ma2 = PostFeatureFactory(feature='x1', feature_value='x3')
    ma3 = PostFeatureFactory(feature='x1', feature_value='x2')
    ma4 = PostFeatureFactory(feature='x1', feature_value='x3')

    assert PostFeature.objects.count() == 2
