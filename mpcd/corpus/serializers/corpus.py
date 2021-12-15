from functools import partial
from app_backend.mpcd.corpus.models import corpus
from app_backend.mpcd.corpus.serializers.sigle import SigleSerializer
from app_backend.mpcd.corpus.serializers.token import TokenSerializer
from app_backend.mpcd.corpus.serializers.author import AuthorSerializer
from app_backend.mpcd.corpus.serializers.codex import CodexSerializer
from app_backend.mpcd.corpus.serializers.edition import EditionSerializer
from ..models import Sigle, Corpus, Resource, Text, Sentence, Author
from rest_framework import serializers

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class CorpusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corpus
        fields = ['id', 'name', 'slug']

class ResourceSerializer(serializers.ModelSerializer):

    authors = AuthorSerializer()

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
        fields = ['id', 'author', 'project', 'reference']


class TextSerializer(serializers.ModelSerializer):

    corpus = serializers.SlugRelatedField(
        queryset=Corpus.objects.all(),
        read_only=True,
        slug_field='slug'
     )

    text_sigle = SigleSerializer()
    editor = AuthorSerializer(many=True, partial=True)
    collaborator = AuthorSerializer(many=True, partial=True)
    resource = ResourceSerializer(partial=True)

    codex_source = CodexSerializer()
    edition_source = EditionSerializer()

    class Meta:
        model = Text
        fields = ['id', 'name', 'text_sigle', 'description', 'resource', 'stage']


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
