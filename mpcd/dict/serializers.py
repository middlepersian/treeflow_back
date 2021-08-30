from rest_framework import serializers
from .models import Entry, Dictionary

class EntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = ('pk','lemma', 'dict')


class DictionarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Dictionary
        fields = ('pk','name', 'slug')
