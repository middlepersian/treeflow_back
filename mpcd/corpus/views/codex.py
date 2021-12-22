from rest_framework import viewsets
from ..models import Codex, Folio, Line
from ..serializers import CodexSerializer, FolioSerializer, LineSerializer
from ..permissions import IsAuthorOrReadOnly


class CodexViewSet(viewsets.ModelViewSet):
    queryset = Codex.objects.all()
    serializer_class = CodexSerializer
    search_fields = ['name', 'slug', 'description', 'scribe', 'library', 'signature', 'facisimile']
    permission_classes = (IsAuthorOrReadOnly,)


class FolioViewSet(viewsets.ModelViewSet):
    queryset = Folio.objects.all()
    serializer_class = FolioSerializer
    search_fields = ['name', 'codex', 'comment']
    permission_classes = (IsAuthorOrReadOnly,)


class LineViewSet(viewsets.ModelViewSet):
    queryset = Line.objects.all()
    serializer_class = LineSerializer
    search_fields = ['number', 'folio', 'comment']
    permission_classes = (IsAuthorOrReadOnly,)