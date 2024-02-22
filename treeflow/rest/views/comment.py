from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from treeflow.corpus.models import Comment
from treeflow.rest.serializers.comment import CommentSerializer
from drf_spectacular.utils import extend_schema

class CommentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

@extend_schema(tags=['comments'])
class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows comments to be viewed.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

