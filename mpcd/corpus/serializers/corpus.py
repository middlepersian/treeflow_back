from .sigle import TextSigleSerializer
from .token import TokenSerializer
from .author import AuthorSerializer
from .codex import CodexSerializer
from .edition import EditionSerializer
from ..models import Corpus, Resource, Source, Text, Sentence, Author, TextSigle
from rest_framework import serializers

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class CorpusSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Corpus.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        return instance

    class Meta:
        model = Corpus
        fields = ['id', 'name', 'slug']


class ResourceSerializer(serializers.ModelSerializer):

    authors = AuthorSerializer(many=True, allow_null=True, partial=True)

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')

        resource_instance, resource_created = Resource.objects.get_or_create(**validated_data)

        for author in authors_data:
            author_instance, author_created = Author.objects.get_or_create(**author)
            resource_instance.authors.add(author_instance)

        return resource_instance

    def update(self, instance, validated_data):

        authors_data = validated_data.pop('authors')

        if authors_data:
            logger.error('UPDATE {}'.format(authors_data))
            for author in authors_data:
                instance.authors.get_or_create(**author)
        else:
            for author in authors_data:
                instance.authors.create(**author)

        instance.save()
        return instance

    class Meta:
        model = Resource
        fields = ['id', 'authors', 'project', 'reference']


class TextSerializer(serializers.ModelSerializer):

    resources = ResourceSerializer(many=True, partial=True, required=False)

    def create(self, validated_data):
        corpus_data = validated_data.pop('corpus')
        text_sigle_data = validated_data.pop('text_sigle')

        resources_data = validated_data.pop('resource')

        sources_data = validated_data.pop('sources')

        corpus_instance = Corpus.objects.get(**corpus_data)
        text_sigle_instance = TextSigle.objects.get(**text_sigle_data)

        text_instance, text_created = Text.objects.create(
            corpus=corpus_instance, text_sigle=text_sigle_instance, **validated_data)


        for resource in resources_data:
            resour, resour_created = Resource.objects.get_or_create(**resource)
            text_instance.resources.add(resour)

        for source in sources_data:
            try:
                source_instance = Source.objects.get(**source)
                text_instance.sources.add(source_instance)
            except Source.DoesNotExist:
                source_instance = Source.objects.create(**source)
                text_instance.sources.add(source_instance)

        return text_instance

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Text
        fields = ['id', 'corpus', 'title', 'text_sigle', 'editors',
                  'collaborators', 'resources', 'stage', 'sources']


class SentenceSerializer(serializers.ModelSerializer):

    text = TextSerializer(partial=True)
    tokens = TokenSerializer(many=True, partial=True)

    class Meta:
        model = Sentence
        fields = ["id", "text", "tokens", "comment"]

    def create(self, validated_data):
        text_data = validated_data.pop('text')
        tokens_data = validated_data.pop('tokens')

        text_instance = Text.objects.create(text=text_data, tokens=tokens_data, **text_data)
        return text_instance

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.tokens = validated_data.get('tokens', instance.tokens)

        instance.save()

        return instance
