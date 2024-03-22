from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from django.db import models
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from treeflow.corpus.models import Section, Token
from treeflow.rest.serializers.section import SectionSerializer, CABSectionSerializer

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

    @action(detail=False, methods=['get'], url_path='identifier/(?P<identifier>.+)', url_name='retrieve_by_identifier')
    @extend_schema(operation_id='retrieve_sections_by_identifier')
    def retrieve_by_identifier(self, request, identifier, *args, **kwargs):
        sections = self.get_queryset().filter(identifier=identifier)
        page = self.paginate_queryset(sections)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['get'], url_path='cab/(?P<identifier>.+)', url_name='retrieve_cab_tokens_by_identifier')
    @extend_schema(operation_id='retrieve_cab_tokens_by_identifier')
    def retrieve_cab_tokens_by_identifier(self, request, identifier, *args, **kwargs):
        sections = self.get_queryset().filter(identifier=identifier).prefetch_related('tokens')
        page = self.paginate_queryset(sections)
        if page is not None:
            serializer = CABSectionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CABSectionSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)