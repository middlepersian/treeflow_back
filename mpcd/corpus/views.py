from rest_framework import viewsets

from .models import BibEntry

from .serializers import BibEntrySerializer
from .permissions import IsAuthorOrReadOnly


class BibEntryViewSet(viewsets.ModelViewSet):
    queryset = BibEntry.objects.all()
    serializer_class = BibEntrySerializer
    search_fields = ['title', 'year']
    permission_classes = (IsAuthorOrReadOnly,)
