from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from treeflow.dict.models import Sense, Lemma
from treeflow.rest.serializers.sense import SenseSerializer
from drf_spectacular.utils import extend_schema


class SensePagination(PageNumberPagination):
    page_size = 100
    
@extend_schema(tags=['senses'])    
class SenseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sense.objects.prefetch_related('related_senses').all()
    pagination_class = SensePagination 
    serializer_class = SenseSerializer

