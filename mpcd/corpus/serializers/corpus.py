import logging
from .sigle import TextSigleSerializer
from .token import TokenSerializer
from .author import AuthorSerializer
from .codex import CodexSerializer
from .edition import EditionSerializer
from ..models import Corpus, Resource, Source, Text, Sentence, Author, TextSigle, Token
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

# import the logging library
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
        lookup_field = 'slug'
        fields = ['name', 'slug']


class ResourceSerializer(serializers.ModelSerializer):

    authors = AuthorSerializer(many=True, allow_null=True, partial=True)

    def create(self, validated_data):

        authors_data = validated_data.pop('authors', None)
        resource_instance, resource_created = Resource.objects.get_or_create(**validated_data)
        if authors_data:
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

    corpus = serializers.SlugRelatedField(slug_field='slug', queryset=Corpus.objects.all())
    text_sigle = serializers.SlugRelatedField(slug_field='sigle', queryset=TextSigle.objects.all())

    resources = ResourceSerializer(many=True, partial=True, required=False)
    sources = serializers.SlugRelatedField(
        slug_field='slug', queryset=Source.objects.all(), many=True, allow_null=True, required=False)

    def create(self, validated_data):
        corpus_data = validated_data.pop('corpus', None)
        text_sigle_data = validated_data.pop('text_sigle', None)

        editors_data = validated_data.pop('editors', None)
        collaborators_data = validated_data.pop('collaborators', None)

        resources_data = validated_data.pop('resources', None)
        sources_data = validated_data.pop('sources', None)

        logger.error('corpus: {}'.format(corpus_data))

        corpus_instance = Corpus.objects.get(slug=corpus_data.slug)
        text_sigle_instance = TextSigle.objects.get(sigle=text_sigle_data.sigle)

        text_instance = Text.objects.create(
            corpus=corpus_instance, text_sigle=text_sigle_instance, **validated_data)

        if resources_data:
            for resource in resources_data:
                resour, resour_created = Resource.objects.get_or_create(**resource)
                text_instance.resources.add(resour)

        if editors_data:
            for editor in editors_data:
                editor_instance, editor_created = User.objects.get_or_create(**editor)
                text_instance.editors.add(editor_instance)

        if collaborators_data:
            for collaborator in collaborators_data:
                collaborator_instance, collaborator_created = User.objects.get_or_create(**collaborator)
                text_instance.collaborators.add(collaborator_instance)

        if sources_data:
            for source in sources_data:
                source_instance = Source.objects.get(slug=source.slug)
                text_instance.sources.add(source_instance)

        return text_instance

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)

        corpus_data = validated_data.pop('corpus', None)
        corpus = instance.corpus
        corpus.slug = corpus_data.slug

        text_sigle_data = validated_data.pop('text_sigle', None)
        text_sigle = instance.text_sigle
        text_sigle.sigle = text_sigle_data.sigle

        editors_data = validated_data.pop('editors', None)
        collaborators_data = validated_data.pop('collaborators', None)
        resources_data = validated_data.pop('resources', None)
        sources_data = validated_data.pop('sources', None)

        if editors_data:
            for editor in editors_data:
                editor_instance, editor_created = User.objects.get_or_create(**editor)
                instance.editors.add(editor_instance)

        if collaborators_data:
            for collaborator in collaborators_data:
                collaborator_instance, collaborator_created = User.objects.get_or_create(**collaborator)
                instance.collaborators.add(collaborator_instance)

        if resources_data:
            for resource in resources_data:
                resour, resour_created = Resource.objects.get_or_create(**resource)
                instance.resources.add(resour)

        if sources_data:
            for source in sources_data:
                source_instance = Source.objects.get(slug=source.slug)
                instance.sources.add(source_instance)

        instance.save()
        return instance

    class Meta:
        model = Text
        fields = ['id', 'corpus', 'title', 'text_sigle', 'editors',
                  'collaborators', 'resources', 'stage', 'sources']


class SentenceSerializer(serializers.ModelSerializer):

    text = serializers.SlugRelatedField(slug_field='title', queryset=Text.objects.all())
    tokens = TokenSerializer(many=True, partial=True, required=False)

    class Meta:
        model = Sentence
        fields = ["id", "text", "tokens", "translation", "comment"]

    def create(self, validated_data):
        text_data = validated_data.pop('text', None)
        tokens_data = validated_data.pop('tokens', None)
        text_instance = Text.objects.get(title=text_data.title)

        sentence_instance = Sentence.objects.create(text=text_instance, **validated_data)

        if tokens_data:
            for token in tokens_data:
                token_instance, token_created = Token.objects.get_or_create(**token)
                sentence_instance.tokens.add(token_instance)
        return sentence_instance

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.translation = validated_data.get('translation', instance.translation)

        tokens_data = validated_data.pop('tokens', None)
        if tokens_data:
            for token in tokens_data:
                token_instance, token_created = Token.objects.get_or_create(**token)
                instance.tokens.add(token_instance)

        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()

        return instance
