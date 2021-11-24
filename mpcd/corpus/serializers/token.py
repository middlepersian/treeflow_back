from rest_framework import serializers
from .. models import Token, Pos


class PosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pos
        fields = ['pos']


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['transcription', 'line', 'position']
