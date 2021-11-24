from rest_framework import serializers
from . import EntrySerializer
from .. models import Token, Pos


class PosSerializer(serializers.ModelSerializer):

    pos = serializers.CharField(max_length=6)

    class Meta:
        model = Pos
        fields = ['pos']


class TokenSerializer(serializers.ModelSerializer):
    transcription = serializers.CharField(max_length=50)
    transliteration = serializers.CharField(max_length=50)
    lemma = EntrySerializer(partial=True, required=False)
    pos = PosSerializer(required=False)

    class Meta:
        model = Token
        fields = ['transcription', 'line', 'position']
