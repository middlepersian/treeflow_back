from rest_framework import viewsets
from ..models import TextSigle
from ..serializers import TextSigleSerializer
from ..permissions import IsAuthorOrReadOnly


class TextSigleViewSet(viewsets.ModelViewSet):
    queryset = TextSigle.objects.all()
    serializer_class = TextSigleSerializer
    search_fields = ['sigle', 'genre']
    permission_classes = (IsAuthorOrReadOnly,)