from rest_framework import viewsets
from ..permissions import IsAuthorOrReadOnly
from ..models import Author
from ..serializers import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    search_fields = ['name', 'last_name']
    permission_classes = (IsAuthorOrReadOnly,)
