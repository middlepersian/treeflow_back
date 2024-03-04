from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from treeflow.corpus.models import Feature
from treeflow.rest.serializers.feature import FeatureSerializer
from drf_spectacular.utils import extend_schema


class FeaturePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

@extend_schema(tags=['features'])
class FeatureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows features to be viewed.
    """
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    pagination_class = FeaturePagination
