from ..models import Codex, Folio, Line
from rest_framework import serializers
from . import AuthorSerializer, BibEntrySerializer


# models/codex.py

class CodexSerializer(serializers.ModelSerializer):

    scribe = AuthorSerializer(many=True, partial=True, required=False)
    facsimile = BibEntrySerializer(many=True, partial=True, required=False)

    class Meta:
        model = Codex
        fields = ['name', 'slug', 'description', 'scribe', 'library', 'signature', 'facisimile']


class FolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folio
        fields = ['name', 'codex', 'comment']


class LineSerializer(serializers.ModelSerializer):
    folio = FolioSerializer(partial=True)

    class Meta:
        model = Line
        fields = ['number', 'folio', 'comment']
