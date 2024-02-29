from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from treeflow.corpus.models import POS
from treeflow.rest.serializers.pos import POSSerializer
from drf_spectacular.utils import extend_schema

class POSPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

@extend_schema(tags=['pos'])
class POSViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows parts of speech to be viewed.
    """
    queryset = POS.objects.all()
    serializer_class = POSSerializer
    pagination_class = POSPagination
