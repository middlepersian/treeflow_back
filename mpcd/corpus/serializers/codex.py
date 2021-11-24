from ..models import Codex, Folio, Line
from rest_framework import serializers
from . import AuthorSerializer, BibEntrySerializer


# models/codex.py

class CodexSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField(unique=True)
    description = serializers.CharField(max_length=255, blank=True)
    scribe = AuthorSerializer(many=True, partial=True, required=False)
    library = serializers.CharField(max_length=100,  blank=True)
    signature = serializers.CharField(max_length=100,  blank=True)
    facsimile = BibEntrySerializer(many=True, partial=True, required=False)

    class Meta:
        model = Codex
        fields = ['name', 'slug', 'description', 'scribe', 'library', 'signature', 'facisimile']


class FolioSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    codex = CodexSerializer(partial=True)
    comment = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Folio
        fields = ['name', 'codex', 'comment']


class LineSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField()
    side = FolioSerializer(partial=True)
    comment = serializers.TextField(required=False)

    class Meta:
        model = Line
        fields = ['number', 'side', 'comment']


class CodexTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = CodexToken
        fields = ['transcription', 'lemma', 'pos', 'features', 'line_id', 'position']

    def create(self, validated_data):
        lemma_data = validated_data.pop('lemma')
        entry_instance = Entry.objects.create(**lemma_data)
        token = Token.objects.create(**validated_data, lemma=entry_instance)

        return token
