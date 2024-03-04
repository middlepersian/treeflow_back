from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from treeflow.corpus.models import Section
from treeflow.rest.serializers.section import SectionSerializer
from drf_spectacular.utils import extend_schema

class SectionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

@extend_schema(tags=['sections'])
class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows sections to be viewed.
    """
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    pagination_class = SectionPagination

