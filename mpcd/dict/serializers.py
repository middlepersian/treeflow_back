from django.utils import translation
from rest_framework import serializers
from .models import Entry, Dictionary, Translation, Category, Word, LoanWord, Reference, Definition

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class DictionarySerializer(serializers.ModelSerializer):

    # name = serializers.CharField(max_length=100)
    slug = serializers.SlugField(max_length=10)

    def create(self, validated_data):
        return Dictionary.create(**validated_data)

    def update(self, instance, validated_data):
        # instance.name = validated_data.get('name', instance.name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        return instance

    class Meta:
        model = Dictionary
        fields = ['id', 'slug']
        extra_kwargs = {
            'slug': {'validators': []}
        }


class TranslationSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Translation.create(**validated_data)

    class Meta:
        model = Translation
        fields = ['id', 'language', 'meaning']
        extra_kwargs = {
            'meaning': {'validators': []}
        }


class CategorySerializer(serializers.ModelSerializer):

    category = serializers.CharField(max_length=10)

    def create(self, validated_data):
        return Category.create(**validated_data)

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance

    class Meta:
        model = Category
        fields = ['id', 'category']
        extra_kwargs = {
            'category': {'validators': []}
        }


class LoanWordSerializer(serializers.ModelSerializer):
    # word = serializers.CharField(max_length=50)
    # language = serializers.CharField(max_length=3)
    translations = TranslationSerializer(many=True, partial=True, required=False)

    def create(self, validated_data):
        translation_data = validated_data.pop('translations')
        word_data = validated_data.pop('word')

        loan_word_instance, word_created = LoanWord.objects.get(word=word_data)
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

    category = serializers.CharField(max_length=10)

    def create(self, validated_data):
        return Category.create(**validated_data)

    def update(self, instance, validated_data):
        instance.reference = validated_data.get('reference', instance.reference)
        instance.save()
        return instance

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

    word = serializers.CharField(max_length=100)
    language = serializers.CharField(max_length=3)

    def create(self, validated_data):
        return Word.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.language = validated_data.get('language', instance.language)
        instance.word = validated_data.get('word', instance.loanwordword)

        instance.save()

        return instance

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
    loanwords = LoanWordSerializer(required=False, many=True, partial=True)
    #translations = TranslationSerializer(required=False, many=True, partial=True)
    # definitions = DefinitionSerializer(many=True, partial=True)
    # categories = CategorySerializer(many=True, partial=True)
    # references = ReferenceSerializer(many=True, partial=True)
    # comment = serializers.JSONField(required=False)

    def create(self, validated_data):

        dict_data = validated_data.pop('dict')
        lemma_data = validated_data.pop('lemma')

        loanwords_data = validated_data.pop('loanwords')
        # translations_data = validated_data.pop('translations')
        # definitions_data = validated_data.pop('definitions')
        # categories_data = validated_data.pop('categories')
        # references_data = validated_data.pop('references')

        dict_instance = Dictionary.objects.get(**dict_data)
        lemma_instance, created = Word.objects.get_or_create(**lemma_data)

        entry_instance, created = Entry.objects.get_or_create(
            lemma=lemma_instance, dict=dict_instance, **validated_data)

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
                            #translats.append(trans)
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

        '''
        for translation in translations_data:
            entry_instance.translations.create(**translation)

        for definition in definitions_data:
            entry_instance.definitions.create(**definition)

        for category in categories_data:
            cat = Category.objects.get(**category)
            entry_instance.categories.add(cat)

        for reference in references_data:
            entry_instance.references.create(**reference)
        '''

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

    class Meta:
        model = Entry
        fields = ['id', 'dict', 'lemma', 'loanwords']

        # 'translations', 'definitions', 'categories', 'references', 'comment']
