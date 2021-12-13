from app_backend.mpcd.corpus.models import corpus
from app_backend.mpcd.corpus.serializers.token import TokenSerializer
from ..models import Author
from rest_framework import serializers
from ..models import Resource, Text, Sentence


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'author', 'project', 'reference']


class TextSerializer(serializers.ModelSerializer):

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
