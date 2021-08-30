from rest_framework import viewsets

from .models import Codex, Folio, Side, Line
from .models import Chapter, Section, Strophe, Verse, Text, Sentence
from .models import Token

from .serializers import TokenSerializer
from .permissions import IsAuthorOrReadOnly

class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (IsAuthorOrReadOnly,)

