from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from treeflow.corpus.models import BibEntry
from treeflow.rest.serializers.bibliography import BibEntrySerializer
from drf_spectacular.utils import extend_schema


class BibEntryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class BibEntryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows bibliography entries to be viewed.
    """
    queryset = BibEntry.objects.all()
    serializer_class = BibEntrySerializer
    pagination_class = BibEntryPagination
