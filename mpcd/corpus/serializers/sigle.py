from ..models import Sigle
from rest_framework import serializers

class SigleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sigle
        fields = ['sigle', 'genre']
