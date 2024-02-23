from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from treeflow.corpus.models import Text
from treeflow.rest.serializers.text import TextSerializer
from drf_spectacular.utils import extend_schema


class TextPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

@extend_schema(tags=['texts'])
class TextViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows texts to be viewed.
    """
    queryset = Text.objects.all()
    serializer_class = TextSerializer
    pagination_class = TextPagination

