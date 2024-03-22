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

import logging

logger = logging.getLogger(__name__)

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
        logger.info(f"Retrieving sections by identifier: {identifier}")
        try:
            sections = self.get_queryset().filter(identifier=identifier)
            if not sections.exists():
                return Response([], status=status.HTTP_404_NOT_FOUND)

            page = self.paginate_queryset(sections)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(sections, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in retrieving sections by identifier: {identifier}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=False, methods=['get'], url_path='cab/(?P<identifier>.+)', url_name='retrieve_cab_tokens_by_identifier')
    @extend_schema(operation_id='retrieve_cab_tokens_by_identifier')
    def retrieve_cab_tokens_by_identifier(self, request, identifier, *args, **kwargs):
        logger.info(f"Retrieving CAB tokens by identifier: {identifier}")
        try:
            sections = Section.objects.filter(identifier=identifier).prefetch_related('tokens')
            if not sections.exists():
                return Response([], status=status.HTTP_404_NOT_FOUND)
            
            serializer = CABSectionSerializer(sections, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in retrieving CAB sections by identifier: {identifier}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)