from rest_framework import viewsets
from .models import Entry, Dictionary
from .serializers import EntrySerializer, DictionarySerializer
from .permissions import IsAuthorOrReadOnly


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (IsAuthorOrReadOnly,)

class DictionaryViewSet(viewsets.ModelViewSet):
    queryset = Dictionary.objects.all()
    serializer_class = DictionarySerializer
    permission_classes = (IsAuthorOrReadOnly,)    

