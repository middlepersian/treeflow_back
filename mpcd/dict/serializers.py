from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import Entry, Dictionary, Lang, Translation, Category, Word, LoanWord, Reference, Definition


class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ('pk', 'name', 'slug')


class LangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lang
        fields = ('pk', 'language', )


class TranslationSerializer(WritableNestedModelSerializer):
    language = LangSerializer(allow_null=True)

    class Meta:
        model = Translation
        fields = ('pk', 'language', 'meaning')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class LoanWordSerializer(WritableNestedModelSerializer):
    language = LangSerializer(allow_null=True)
    translation = TranslationSerializer(many=True)

    class Meta:
        model = LoanWord
        fields = ('pk', 'word', 'language', 'translation')


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ('pk', 'reference', 'url')


class DefinitionSerializer(WritableNestedModelSerializer):
    language = LangSerializer(allow_null=True)

    class Meta:
        model = Definition
        fields = ('pk', 'definition', 'language')


class EntrySerializer(WritableNestedModelSerializer):

    dict = DictionarySerializer()
    loanword = LoanWordSerializer(allow_null=True)
    translation = TranslationSerializer(many=True)
    definition = DefinitionSerializer(many=True)
    category = CategorySerializer(many=True)
    literature = ReferenceSerializer(many=True)
    #cross_reference = WordSerializer(many=True)

    class Meta:
        model = Entry
        fields = ('pk', 'dict', 'loanword', 'translation', 'definition',
                  'category', 'literature', 'comment', 'cross_reference')


class WordSerializer(WritableNestedModelSerializer):

    language = LangSerializer(allow_null=True)

    # Reverse OneToOne relationship
    entry = EntrySerializer()

    class Meta:
        model = Word
        fields = ('pk', 'word', 'language', 'entry')
