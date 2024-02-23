from rest_framework import serializers
from treeflow.corpus.models import Feature

class FeatureSerializer(serializers.ModelSerializer):
    
        class Meta:
    
            model = Feature
            fields = '__all__'
