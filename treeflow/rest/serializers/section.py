from rest_framework import serializers
from treeflow.corpus.models import Section, Token


class TokenSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Token
            fields = ('id', 'transcription',)

class SectionSerializer(serializers.ModelSerializer):

    text_identifier = serializers.CharField(source='text.identifier', read_only=True)
    tokens = TokenSerializer(many=True, read_only=True)
    class Meta:
        model = Section
        fields = '__all__'

