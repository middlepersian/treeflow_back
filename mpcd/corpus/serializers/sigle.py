from ..models import TextSigle
from rest_framework import serializers

class TextSigleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextSigle
        fields = ['sigle', 'genre']
