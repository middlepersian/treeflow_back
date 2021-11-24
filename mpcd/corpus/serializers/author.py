from ..models import Author
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=30)

    class Meta:
        model = Author
        fields = ['name', 'last_name']
