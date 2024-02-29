from django.db.models import Prefetch
from rest_framework import serializers
from treeflow.dict.models import Sense, Lemma

class SenseSerializer(serializers.ModelSerializer):
    related_senses = serializers.PrimaryKeyRelatedField(queryset=Sense.objects.all(), many=True)

    class Meta:
        model = Sense
        fields = ('id', 'lemma_related', 'sense', 'language', 'related_senses')
        read_only_fields = ('id',)