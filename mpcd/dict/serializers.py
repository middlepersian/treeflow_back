from rest_framework import serializers
from .models import Entry, Dictionary, Translation, Category, Word, LoanWord, Reference, Definition

import logging


class DictionarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Dictionary
        fields = ['id', 'slug']
        extra_kwargs = {
            'slug': {'validators': []}
        }


class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['language', 'meaning']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class LoanWordSerializer(serializers.ModelSerializer):
    translation = TranslationSerializer(many=True)

    class Meta:
        model = LoanWord
        fields = ['word', 'language', 'translation']


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ['reference', 'url']


class DefinitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Definition
        fields = ['definition', 'language']


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ('id', 'word', 'language')
        extra_kwargs = {
            'word': {'validators': []}
        }


class EntrySerializer(serializers.ModelSerializer):

    dict = DictionarySerializer()
    lemma = WordSerializer()
    #lang = LangSerializer()
    #loanword = LoanWordSerializer(allow_null=True)
    #translation = TranslationSerializer(many=True)
    #definition = DefinitionSerializer(many=True)
    #category = CategorySerializer(many=True)
    #literature = ReferenceSerializer(many=True)
    #cross_reference = WordSerializer(many=True)

    def create(self, validated_data):

        dict_data = validated_data.pop('dict')
        lemma_data = validated_data.pop('lemma')

        dict_instance = Dictionary.objects.get(**dict_data)
        lemma_instance = Word.objects.create(**lemma_data)

        entry_instance = Entry.objects.create(lemma=lemma_instance, dict=dict_instance)

        return entry_instance

    class Meta:
        model = Entry
        fields = ['id', 'dict', 'lemma']
        
