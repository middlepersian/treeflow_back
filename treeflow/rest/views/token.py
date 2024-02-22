from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from treeflow.corpus.models import Token
from treeflow.rest.serializers.token import TokenSerializer
from drf_spectacular.utils import extend_schema


class TokenPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

@extend_schema(tags=['tokens'])
class TokenViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows tokens to be viewed.
    """
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    pagination_class = TokenPagination
