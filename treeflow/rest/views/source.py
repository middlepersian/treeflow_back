from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from treeflow.corpus.models import Source
from treeflow.rest.serializers.source import SourceSerializer
from drf_spectacular.utils import extend_schema


class SourcePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

@extend_schema(tags=['sources'])
class SourceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows sources to be viewed.
    """
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

