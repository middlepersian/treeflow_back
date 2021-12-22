from rest_framework import viewsets
from ..permissions import IsAuthorOrReadOnly
from .. models import BibEntry
from .. serializers import BibEntrySerializer


class BibEntryViewSet(viewsets.ModelViewSet):
    queryset = BibEntry.objects.all()
    serializer_class = BibEntrySerializer
    search_fields = ['title', 'year']
    permission_classes = (IsAuthorOrReadOnly,)
