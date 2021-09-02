from rest_framework import viewsets

from .models import Codex, Folio, Side, Line
from .models import Chapter, Section, Strophe, Verse, Text, Sentence
from .models import CodexToken

from .serializers import CodexTokenSerializer
from .permissions import IsAuthorOrReadOnly


class CodexTokenViewSet(viewsets.ModelViewSet):
    queryset = CodexToken.objects.all()
    serializer_class = CodexTokenSerializer
    permission_classes = (IsAuthorOrReadOnly,)