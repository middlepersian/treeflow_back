from rest_framework import serializers
from treeflow.dict.models import Lemma, Sense
from treeflow.rest.serializers.sense import SenseSerializer

class LemmaSerializer(serializers.ModelSerializer):
    related_senses = SenseSerializer(many=True)
    related_lemmas = serializers.PrimaryKeyRelatedField(queryset=Lemma.objects.all(), many=True)
    class Meta:
        model = Lemma
        fields = '__all__'
