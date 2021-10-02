from mpcd.dict.models.dictionary import Category, Definition, Reference, Translation
from rest_framework import viewsets, filters, permissions
from .models import Entry, Dictionary, Word, LoanWord
from .serializers import DefinitionSerializer, EntrySerializer, DictionarySerializer, ReferenceSerializer, WordSerializer, \
    LoanWordSerializer, TranslationSerializer, CategorySerializer
from .permissions import IsAuthorOrReadOnly


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticated,)

class DictionaryViewSet(viewsets.ModelViewSet):
    queryset = Dictionary.objects.all()
    serializer_class = DictionarySerializer
    permission_classes = (permissions.IsAuthenticated,)

class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['word','language']
    permission_classes = (permissions.IsAuthenticated,)

class LoanWordViewSet(viewsets.ModelViewSet):
    queryset = LoanWord.objects.all()
    serializer_class = LoanWordSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['word','language']
    permission_classes = (permissions.IsAuthenticated,)

class TranslationViewSet(viewsets.ModelViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['meaning','language']
    permission_classes = (permissions.IsAuthenticated,)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)

class DefinitionViewSet(viewsets.ModelViewSet):
    queryset = Definition.objects.all()
    serializer_class = DefinitionSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = (permissions.IsAuthenticated,)
