from rest_framework import serializers
from treeflow.corpus.models import BibEntry

#serializer for BibEntry
class BibEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = BibEntry
        fields = '__all__'
