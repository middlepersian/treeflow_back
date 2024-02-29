from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from treeflow.dict.models import Lemma
from treeflow.rest.serializers.lemma import LemmaSerializer
from drf_spectacular.utils import extend_schema

class LemmaPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

@extend_schema(tags=['lemmas'])
class LemmaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lemma.objects.prefetch_related('related_senses', 'related_lemmas').all()

    serializer_class = LemmaSerializer
    pagination_class = LemmaPagination 
