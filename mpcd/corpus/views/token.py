from rest_framework import viewsets
from ..models import MorphologicalAnnotation, Dependency, Token
from ..serializers import MorphologicalAnnotationSerializer, DependencySerializer, TokenSerializer
from ..permissions import IsAuthorOrReadOnly


class MorphologicalAnnotationViewSet(viewsets.ModelViewSet):
    queryset = MorphologicalAnnotation.objects.all()
    serializer_class = MorphologicalAnnotationSerializer
    search_fields = ['feature', 'feature_value']
    permission_classes = (IsAuthorOrReadOnly,)


class DependencyViewSet(viewsets.ModelViewSet):
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer
    search_fields = ['head', 'rel']
    permission_classes = (IsAuthorOrReadOnly,)


class TokenViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = Token.objects.all()
        queryset = queryset.prefetch_related('lemma')
        queryset = queryset.select_related('pos')
        queryset = queryset.prefetch_related('morphological_annotation')
        queryset = queryset.prefetch_related('syntactic_annotation')
        queryset = queryset.select_related('previous')

        return queryset

    serializer_class = TokenSerializer
    search_fields = ['transcription', 'transliteration', 'lemma',
                     'pos', 'morphological_annotation', 'syntactic_annotation', 'comment', 'previous']
    permission_classes = (IsAuthorOrReadOnly,)
