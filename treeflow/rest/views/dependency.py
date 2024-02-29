from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from treeflow.corpus.models import Dependency
from treeflow.rest.serializers.dependency import DependencySerializer
from drf_spectacular.utils import extend_schema

class DependencyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

@extend_schema(tags=['dependencies'])
class DependencyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows dependencies to be viewed.
    """
    pagination_class = DependencyPagination
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer
