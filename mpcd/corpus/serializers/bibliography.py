from ..models import Author
from rest_framework import serializers
from . import AuthorSerializer

# models/bibliography.py

class BibEntrySerializer():

    authors = AuthorSerializer(many=True, partial=True, required=False)
    title = serializers.CharField(max_length=100)
    year = serializers.PositiveSmallIntegerField(partial=True, required=False)

    class Meta:
        model = Author
        fields = ['authors', 'title', 'year']
