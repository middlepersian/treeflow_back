from django.utils import translation
from rest_framework import serializers
from .models import Entry, Dictionary, Translation, Category, Word, LoanWord, Reference, Definition

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class DictionarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Dictionary
        fields = ['slug']
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
        fields = ['category']
        extra_kwargs = {
            'category': {'validators': []}
        }


class LoanWordSerializer(serializers.ModelSerializer):
    translation = TranslationSerializer(many=True)

    def create(self, validated_data):
        translation_data = validated_data.pop('translations')
        translation_instance = Translation.objects.create(**translation_data)
        loan_word_instance = LoanWord.objects.create(translation=translation_instance, **validated_data)

        return loan_word_instance

    class Meta:
        model = LoanWord
        fields = ['word', 'language', 'translations']
        extra_kwargs = {
            'word': {'validators': []}
        }


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
        fields = ('word', 'language')
        extra_kwargs = {
            'word': {'validators': []}
        }


class EntrySerializer(serializers.ModelSerializer):

    dict = DictionarySerializer()
    lemma = WordSerializer()
    loanwords = LoanWordSerializer(many=True)
    translations = TranslationSerializer(many=True)
    definitions = DefinitionSerializer(many=True)
    categories = CategorySerializer(many=True)
    references = ReferenceSerializer(many=True)

    def create(self, validated_data):

        dict_data = validated_data.pop('dict')
        lemma_data = validated_data.pop('lemma')
        loanwords_data = validated_data.pop('loanwords')
        translations_data = validated_data.pop('translations')
        definitions_data = validated_data.pop('definitions')
        categories_data = validated_data.pop('categories')
        references_data = validated_data.pop('references')

        dict_instance = Dictionary.objects.get(**dict_data)
        lemma_instance = Word.objects.create(**lemma_data)

        entry_instance = Entry.objects.create(lemma=lemma_instance, dict=dict_instance)

        for loanword in loanwords_data:
            entry_instance.loanwords.create(**loanword)

        for translation in translations_data:
            entry_instance.translations.create(**translation)

        for definition in definitions_data:
            entry_instance.definitions.create(**definition)

        for category in categories_data:
            cat = Category.objects.get(**category)
            entry_instance.categories.add(cat)

        for reference in references_data:
            entry_instance.references.create(**reference)

        return entry_instance
       
    class Meta:
        model = Entry
        fields = ['dict', 'lemma', 'loanwords', 'translations', 'definitions', 'categories', 'references']
