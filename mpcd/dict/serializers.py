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
        fields = ['id', 'slug']
        extra_kwargs = {
            'slug': {'validators': []}
        }


class TranslationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Translation
        fields = ['id', 'language', 'meaning']
        extra_kwargs = {
            'meaning': {'validators': []}
        }


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'category']
        extra_kwargs = {
            'category': {'validators': []}
        }


class LoanWordSerializer(serializers.ModelSerializer):

    translations = TranslationSerializer(many=True, partial=True, required=False)

    def create(self, validated_data):
        translation_data = validated_data.pop('translations')
        word_data = validated_data.pop('word')
        loan_word_instance, word_created = LoanWord.objects.get_or_create(word=word_data)

        if not word_created:
            logger.error('loanword does not exist')
            loan_word_instance = LoanWord.objects.create(**validated_data)

        for translation in translation_data:
            trans, trans_created = Translation.objects.get_or_create(**translation)
            logger.error('translations does not exist')

            if not trans_created:
                loan_word_instance.translations.add(trans)

        return loan_word_instance

    def update(self, instance, validated_data):

        instance.word = validated_data.get('word', instance.word)
        instance.language = validated_data.get('language', instance.language)

        translations_data = validated_data.pop('translations')

        for translation in translations_data:
            instance.translations.update(**translation)

        instance.save()

        return instance

    class Meta:
        model = LoanWord
        fields = ['id', 'word', 'language', 'translations']
        extra_kwargs = {
            'word': {'validators': []},
            'translations': {'validators': []}
        }
class ReferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reference
        fields = ['id', 'reference', 'url']
        extra_kwargs = {
            'reference': {'validators': []}
        }


class DefinitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Definition
        fields = ['id', 'definition', 'language']
        extra_kwargs = {
            'definition': {'validators': []}
        }


class WordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Word
        fields = ('id', 'word', 'language')
        extra_kwargs = {
            'word': {'validators': []},
            'language': {'validators': []}
        }


class EntrySerializer(serializers.ModelSerializer):

    dict = DictionarySerializer()
    lemma = WordSerializer()
    loanwords = LoanWordSerializer(many=True, required=False)
    translations = TranslationSerializer(many=True, required=False)
    definitions = DefinitionSerializer(many=True, partial=True, required=False)
    categories = CategorySerializer(many=True, partial=True, required=False)
    references = ReferenceSerializer(many=True, partial=True, required=False)

    class Meta:
        model = Entry
        fields = ['id', 'dict', 'lemma', 'loanwords', 'translations',
                  'definitions', 'categories', 'references', 'comment']

    def create(self, validated_data):

        dict_data = validated_data.pop('dict')
        lemma_data = validated_data.pop('lemma')

        loanwords_data = validated_data.pop('loanwords')
        translations_data = validated_data.pop('translations')
        definitions_data = validated_data.pop('definitions')
        categories_data = validated_data.pop('categories')
        references_data = validated_data.pop('references')

        dict_instance = Dictionary.objects.get(**dict_data)
        lemma_instance, lemma_created = Word.objects.get_or_create(**lemma_data)
        entry_instance, entry_created = Entry.objects.get_or_create(
            lemma=lemma_instance, dict=dict_instance, **validated_data)

        # loanword is treated differently due to the pointer to translation inside this model
        for loanword in loanwords_data:
            word_data = loanword.get('word')
            logger.error('WORD DATA {} {}'.format(word_data, type(word_data)))

            # check if loanword exists
            try:
                loan_word_instance = LoanWord.objects.get(word=word_data)
            # if not, create it
            except LoanWord.DoesNotExist:
                logger.error('loanword does not exist')

                translats = []
                if loanword.get('translations'):
                    logger.error('TRANS: {}'.format(loanword.get('translations')))
                    translation_data = loanword.pop('translations')
                    for translation in translation_data:
                        try:
                            trans = Translation.objects.get(**translation)
                            # translats.append(trans)
                        except Translation.DoesNotExist:
                            logger.error('translation does not exist')
                            trans = Translation.objects.create(**translation)
                            translats.append(trans)

                if translats:
                    loan_word_instance = LoanWord.objects.create(**loanword)
                    for translat in translats:
                        loan_word_instance.translations.add(translat)
                else:
                    loan_word_instance = LoanWord.objects.create(**loanword)

            entry_instance.loanwords.add(loan_word_instance)

        # logger.error('CREATE {}'.format(lw))

        for translation in translations_data:
            translat, translat_created = Translation.objects.get_or_create(**translation)
            entry_instance.translations.add(translat)

        for definition in definitions_data:
            defin, defin_created = Definition.objects.get_or_create(**definition)
            entry_instance.definitions.add(defin)

        for category in categories_data:
            cat, cat_created = Category.objects.get_or_create(**category)
            entry_instance.categories.add(cat)

        for reference in references_data:
            ref, ref_created = Reference.objects.get_or_create(**reference)
            entry_instance.references.add(ref)

        return entry_instance

    def update(self, instance, validated_data):

        dict_data = validated_data.pop('dict')
        dict = instance.dict
        dict.name = dict_data.get('name', dict.name)
        dict.slug = dict_data.get('slug', dict.slug)
        dict.save()

        lemma_data = validated_data.pop('lemma')
        lemma = instance.lemma
        lemma.word = lemma_data.get('word', lemma.word)
        lemma.language = lemma_data.get('language', lemma.language)
        lemma.save()

        # TODO check if this works with translations
        loanwords_data = validated_data.pop('loanwords')
        if loanwords_data:
            logger.error('UPDATE {}'.format(loanwords_data))
            for loanword in loanwords_data:
                instance.loanwords.get_or_create(**loanword)
        else:
            for loanword in loanwords_data:
                instance.loanwords.create(**loanword)

        instance.save()

        return instance
