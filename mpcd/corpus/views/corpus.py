from rest_framework import viewsets
from ..models import Corpus, Resource, Text, Sentence
from ..serializers import CorpusSerializer, ResourceSerializer, TextSerializer, SentenceSerializer
from ..permissions import IsAuthorOrReadOnly


class CorpusViewSet(viewsets.ModelViewSet):
    queryset = Corpus.objects.all()
    serializer_class = CorpusSerializer
    lookup_field = 'slug'
    search_fields = ['name', 'slug']
    permission_classes = (IsAuthorOrReadOnly,)


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    search_fields = ['authors', 'description', 'project', 'reference']
    permission_classes = (IsAuthorOrReadOnly,)


class TextViewSet(viewsets.ModelViewSet):
    queryset = Text.objects.all()
    serializer_class = TextSerializer
    search_fields = ['title', 'text_sigle', 'editor', 'collaborator',
                     'resource', 'stage', 'codex_source', 'edition_source']
    permission_classes = (IsAuthorOrReadOnly,)


class SentenceViewSet(viewsets.ModelViewSet):
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer
    search_fields = ['text', 'tokens', 'translation', 'comment']
    permission_classes = (IsAuthorOrReadOnly,)
