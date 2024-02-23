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
    queryset = Comment.objects.select_related('user', 'dependency', 'image', 'section', 'source', 'token', 'text', 'lemma', 'sense', 'semantic')\
                              .prefetch_related('user__comment_user', 'dependency__comment_dependency', 'image__comment_image', 
                                                'section__comment_section', 'source__comment_source', 'token__comment_token', 
                                                'text__comment_text', 'lemma__comment_lemma', 'sense__comment_sense', 
                                                'semantic__comment_semantic')\
                              .all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination