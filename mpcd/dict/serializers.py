from rest_framework import serializers
from .models import Entry, Dictionary, Lang, Translation, Category, Word, LoanWord, Reference, Definition

class EntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = ('pk','lemma', 'dict','loanword','translation','definition','category','literature','comment','cross_reference')


class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ('pk','name', 'slug')


class LangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lang
        fields = '__all__'

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ('pk','language','meaning')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ('pk','word', 'language')

class LoanWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanWord
        fields = ('pk','word', 'language','translation')

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ('pk','reference','url')

class DefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definition
        fields = ('pk','definition','language')
