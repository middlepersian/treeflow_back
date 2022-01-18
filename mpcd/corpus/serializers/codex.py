from ..models import Codex, Folio, Line, Author, BibEntry
from rest_framework import serializers
from . import AuthorSerializer, BibEntrySerializer


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


# models/codex.py

class CodexSerializer(serializers.ModelSerializer):

    scribe = AuthorSerializer(many=True, partial=True, required=False, allow_null=True)
    facsimile = BibEntrySerializer(many=True, partial=True, required=False)

    def create(self, validated_data):
        scribe_data = validated_data.pop('scribe', None)
        facsimile_data = validated_data.pop('facsimile', None)
        codex_instance, codex_created = Codex.objects.get_or_create(**validated_data)

        if scribe_data:
            for scribe in scribe_data:
                scri, scri_created = Author.objects.get_or_create(**scribe)
                codex_instance.scribe.add(scri)

        if facsimile_data:
            for facsimile in facsimile_data:
                facs, facs_created = BibEntry.objects.get_or_create(**facsimile)
                codex_instance.facsimile.add(facs)

        return codex_instance

    def update(self, instance, validated_data):

        scribe_data = validated_data.pop('scribe', None)
        if scribe_data:
            logger.error('UPDATE {}'.format(scribe_data))
            for scribe in scribe_data:
                instance.scribe.get_or_create(**scribe)

        facsimile_data = validated_data.pop('facsimile', None)
        if facsimile_data:
            logger.error('UPDATE {}'.format(facsimile_data))
            for facsimile in facsimile_data:
                instance.facsimile.get_or_create(**facsimile)

        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.description = validated_data.get('description', instance.description)
        instance.copy_date = validated_data.get('copy_date', instance.copy_date)
        instance.copy_place_name = validated_data.get('copy_place_name', instance.copy_place_name)
        instance.copy_place_latitude = validated_data.get('copy_place_latitude', instance.copy_place_latitude)
        instance.library = validated_data.get('library', instance.library)
        instance.signature = validated_data.get('signature', instance.signature)

        instance.save()
        return instance

    class Meta:
        model = Codex
        fields = ['id', 'name', 'slug', 'sigle', 'description', 'copy_date',
                  'copy_place_name', 'copy_place_latitude', 'copy_place_longitude', 'scribe', 'library', 'signature', 'facsimile']


class FolioSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

        codex_data = validated_data.pop('codex')
        codex_instance, codex_created = Codex.objects.get_or_create(**codex_data)
        folio_instance, folio_created = Folio.objects.get_or_create(**validated_data, codex=codex_instance)

        return folio_instance

    def update(self, instance, validated_data):

        codex_data = validated_data.pop('codex')
        codex = instance.codex
        codex.name = codex_data.get('name', dict.name)
        codex.slug = codex_data.get('slug', dict.slug)
        codex.save()

        instance.save()

    class Meta:
        model = Folio
        fields = ['id', 'name', 'codex', 'comment']


class LineSerializer(serializers.ModelSerializer):

    folio = FolioSerializer(partial=True)

    def create(self, validated_data):
        folio_data = validated_data.pop('folio')
        folio_instance, folio_created = Line.objects.get_or_create(**folio_data)
        line_instance, line_created = Line.objects.get_or_create(**validated_data, folio=folio_instance)
        return line_instance

    def update(self, instance, validated_data):
        folio_data = validated_data.pop('folio')
        folio = instance.folio
        folio.identifier = folio_data.get('identifier', folio.identifier)
        folio.codex = folio_data.get('codex', folio.codex)
        folio.save()

        instance.save()

    class Meta:
        model = Line
        fields = ['id', 'number', 'folio', 'comment']
