from mpcd.codex.models.physical import CodexToken
from rest_framework import serializers
from .models import Token
from mpcd.dict.serializers import EntrySerializer
from mpcd.dict.models import Entry



class CodexTokenSerializer(serializers.ModelSerializer):

    lemma = EntrySerializer()

    class Meta:
        model = CodexToken
        fields = ('transcription', 'lemma', 'pos', 'features', 'line_id', 'position')

    def create(self, validated_data):
        lemma_data = validated_data.pop('lemma')
        entry_instance =  Entry.objects.create(**lemma_data)
        token = Token.objects.create(**validated_data, lemma=entry_instance)

        return token
