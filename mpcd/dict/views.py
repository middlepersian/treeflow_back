from mpcd.dict.models.dictionary import Category, Definition, Reference, Translation
from rest_framework import viewsets, filters, permissions, status
from rest_framework.response import Response
from .models import Entry, Dictionary, Word, LoanWord
from .serializers import DefinitionSerializer, EntrySerializer, DictionarySerializer, ReferenceSerializer, WordSerializer, \
    LoanWordSerializer, TranslationSerializer, CategorySerializer
from .permissions import IsAuthorOrReadOnly


class DictionaryViewSet(viewsets.ModelViewSet):
    queryset = Dictionary.objects.all()
    serializer_class = DictionarySerializer
    permission_classes = (IsAuthorOrReadOnly,)


class EntryViewSet(viewsets.ModelViewSet):

    queryset = (
        Entry.objects
        .select_related(
            'dict', 'lemma'
        ).prefetch_related(
            'loanwords',
            'translations',
            'definitions',
            'categories',
            'references'
        ).order_by('lemma')
    )
    serializer_class = EntrySerializer
    permission_classes = (IsAuthorOrReadOnly,)


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['word', 'language']
    permission_classes = (IsAuthorOrReadOnly,)


class LoanWordViewSet(viewsets.ModelViewSet):
    queryset = (LoanWord.objects.prefetch_related('translations'))
    serializer_class = LoanWordSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['word', 'language']
    permission_classes = (IsAuthorOrReadOnly,)

    def create(self, request):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TranslationViewSet(viewsets.ModelViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['meaning', 'language']
    permission_classes = (IsAuthorOrReadOnly,)

    def create(self, request):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def create(self, request):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DefinitionViewSet(viewsets.ModelViewSet):
    queryset = Definition.objects.all()
    serializer_class = DefinitionSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def create(self, request):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def create(self, request):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
