from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from treeflow.corpus.models import Section
from treeflow.rest.serializers.section import SectionSerializer

class SectionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


@extend_schema(tags=['sections'])
class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows sections to be viewed or retrieved by ID or identifier.
    """
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    pagination_class = SectionPagination

    @extend_schema(operation_id='retrieve_section_by_identifier')
    def retrieve_by_identifier(self, request, *args, **kwargs):
        identifier = kwargs.get('identifier')
        obj = get_object_or_404(self.get_queryset(), identifier=identifier)
        self.check_object_permissions(request, obj)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)