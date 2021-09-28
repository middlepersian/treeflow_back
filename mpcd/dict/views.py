from mpcd.dict.models.dictionary import Category, Definition, Reference, Translation
from rest_framework import viewsets, filters
from .models import Entry, Dictionary, Word, LoanWord, Lang
from .serializers import DefinitionSerializer, EntrySerializer, DictionarySerializer, ReferenceSerializer, WordSerializer, \
    LoanWordSerializer, LangSerializer, TranslationSerializer, CategorySerializer
from .permissions import IsAuthorOrReadOnly


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (IsAuthorOrReadOnly,)

class DictionaryViewSet(viewsets.ModelViewSet):
    queryset = Dictionary.objects.all()
    serializer_class = DictionarySerializer
    permission_classes = (IsAuthorOrReadOnly,)

class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['word','language__language']
    permission_classes = (IsAuthorOrReadOnly,)

class LoanWordViewSet(viewsets.ModelViewSet):
    queryset = LoanWord.objects.all()
    serializer_class = LoanWordSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['word','language__language']
    permission_classes = (IsAuthorOrReadOnly,)

class LangViewSet(viewsets.ModelViewSet):
    queryset = Lang.objects.all()
    serializer_class = LangSerializer
    permission_classes = (IsAuthorOrReadOnly,)

class TranslationViewSet(viewsets.ModelViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['meaning','language__language']
    permission_classes = (IsAuthorOrReadOnly,)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthorOrReadOnly,)

class DefinitionViewSet(viewsets.ModelViewSet):
    queryset = Definition.objects.all()
    serializer_class = DefinitionSerializer
    permission_classes = (IsAuthorOrReadOnly,)

class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = (IsAuthorOrReadOnly,)
