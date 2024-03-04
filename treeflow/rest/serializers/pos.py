from rest_framework import serializers
from treeflow.corpus.models import POS

class POSSerializer(serializers.ModelSerializer):
        
            class Meta:
                model = POS        
                fields = '__all__'
