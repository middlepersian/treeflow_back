from rest_framework import viewsets
from ..models import FeatureValue, Feature, MorphologicalAnnotation, Dependency, SyntacticAnnotation, Pos, Token
from ..serializers import FeatureValueSerializer, FeatureSerializer, MorphologicalAnnotationSerializer, DependencySerializer, SyntacticAnnotationSerializer, PosSerializer, TokenSerializer
from ..permissions import IsAuthorOrReadOnly


class FeatureValueViewSet(viewsets.ModelViewSet):
    queryset = FeatureValue.objects.all()
    serializer_class = FeatureValueSerializer
    search_fields = ['name']
    permission_classes = (IsAuthorOrReadOnly,)


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    search_fields = ['name']
    permission_classes = (IsAuthorOrReadOnly,)


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


class SyntacticAnnotationViewSet(viewsets.ModelViewSet):
    queryset = SyntacticAnnotation.objects.all()
    serializer_class = SyntacticAnnotationSerializer
    search_fields = ['dependency']
    permission_classes = (IsAuthorOrReadOnly,)


class PosViewSet(viewsets.ModelViewSet):
    queryset = Pos.objects.all()
    serializer_class = PosSerializer
    search_fields = ['pos']
    permission_classes = (IsAuthorOrReadOnly,)


class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    search_fields = ['transcription', 'transliteration', 'lemma',
                     'pos', 'features', 'syntax_annotations', 'comment', 'previous']
    permission_classes = (IsAuthorOrReadOnly,)
