from rest_framework import serializers
from treeflow.corpus.models import Section, Token
from treeflow.corpus.management.commands.newparts import get_tokens_between_subsections


class SectionTokenSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Token
            fields = ('id', 'transcription',)

class SectionSerializer(serializers.ModelSerializer):

    text_identifier = serializers.CharField(source='text.identifier', read_only=True)

    def get_tokens(self, obj):
        if obj.type == "subsubsection":
            # Call your method to get the tokens for "subsubsection"
            tokens = get_tokens_between_subsections(obj.identifier)
        else:
            # Return the regular tokens for other types
            tokens = obj.tokens.all()
        return SectionTokenSerializer(tokens, many=True).data
    
    tokens = serializers.SerializerMethodField()
    class Meta:
        model = Section
        fields = '__all__'

