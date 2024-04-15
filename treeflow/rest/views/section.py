from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.shortcuts import get_object_or_404
from django.db import models
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from treeflow.corpus.models import Section, Token, Text
from treeflow.rest.serializers.section import TokenSerializer, SectionSerializer

import logging

logger = logging.getLogger(__name__)

class SectionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

@extend_schema(tags=['sections'])
class SectionViewSet(viewsets.GenericViewSet):
    serializer_class = SectionSerializer
    pagination_class = SectionPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(name='identifier', description='Filter by section identifier', required=False, type=str),
            OpenApiParameter(name='text_identifier', description='Filter by text identifier', required=False, type=str),
            OpenApiParameter(name='type', description='Filter by section type when text_identifier is present', required=False, type=str)
        ],
        responses={200: SectionSerializer(many=True)})
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()  # Apply the filters right from the get_queryset

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Section.objects.all()
        identifier = self.request.query_params.get('identifier')
        text_identifier = self.request.query_params.get('text_identifier')
        type = self.request.query_params.get('type')

        # Utilizing the unique constraint for filtering by 'text' and 'identifier'
        if text_identifier and identifier:
            queryset = queryset.filter(text__identifier=text_identifier, identifier=identifier)
            logger.debug(f"Filtered by text identifier and section identifier: {text_identifier}, {identifier}")

        # Utilizing the index for filtering by 'text' and 'type'
        elif text_identifier and type:
            queryset = queryset.filter(text__identifier=text_identifier, type=type)
            logger.debug(f"Filtered by text identifier and type: {text_identifier}, {type}")

        # Additional filters for identifier or type alone
        else:
            if identifier:
                queryset = queryset.filter(identifier=identifier)
                logger.debug(f"Filtered by identifier: {identifier}")
            if text_identifier:
                queryset = queryset.filter(text__identifier=text_identifier)
                logger.debug(f"Filtered by text identifier: {text_identifier}")
            if type:
                queryset = queryset.filter(type=type)
                logger.debug(f"Filtered by type: {type}")

        return queryset
