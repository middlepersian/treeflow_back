from rest_framework import serializers
from .models import Codex, Folio, Side, Line
from .models import Text, Chapter, Section, Sentence, Strophe, Verse
from .models import Token, MorphologicalAnnotation
from mpcd.dict.serializers import EntrySerializer
from mpcd.dict.models import Entry


class TokenSerializer(serializers.ModelSerializer):

    lemma = EntrySerializer()

    class Meta:
        model = Token
        fields = ('token', 'lemma', 'morph_annotations')

    def create(self, validated_data):
        lemma_data = validated_data.pop('lemma')
        entry_instance =  Entry.objects.create(**lemma_data)
        token = Token.objects.create(**validated_data, lemma=entry_instance)

        return token
