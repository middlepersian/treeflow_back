from rest_framework import viewsets
from ..models import Edition
from ..serializers import EditionSerializer
from ..permissions import IsAuthorOrReadOnly


class EditionViewSet(viewsets.ModelViewSet):
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer
    search_fields = ['name', 'auhtors', 'references', 'text_sigle', 'description']
    permission_classes = (IsAuthorOrReadOnly,)
