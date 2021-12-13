from rest_framework import serializers
from .. models import FeatureValue, Feature, MorphologicalAnnotation, Dependency, \
    SyntacticAnnotation, Pos, Token

from mpcd.dict.serializers import EntrySerializer

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class FeatureValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureValue
        fields = ['name']


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['name']


class MorphologicalAnnotationSerializer(serializers.ModelSerializer):

    feature = FeatureSerializer()
    feature_value = FeatureValueSerializer()

    class Meta:
        model = MorphologicalAnnotation
        fields = ['feature', 'feature_value']

    def create(self, validated_data):
        feature_value_data = validated_data.pop('feature')
        feature_data = validated_data.pop('feature_value')

        morph_instance = MorphologicalAnnotation.objects.create(
            feature=feature_data, feature_value=feature_value_data, **validated_data)

        return morph_instance

    def update(self, instance, validated_data):

        instance.feature = validated_data.get('feature', instance.feature)
        instance.feature_value = validated_data.get('feature_value', instance.feature_value)

        instance.save()

        return instance


class DependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['head', 'rel']


class SyntacticAnnotationSerializer(serializers.ModelSerializer):

    dependency = DependencySerializer(required=False)

    def create(self, validated_data):
        depndency_data = validated_data.pop('dependency')

        depndency_instance = MorphologicalAnnotation.objects.create(dependency=depndency_data, **validated_data)

        return depndency_instance

    def update(self, instance, validated_data):

        instance.dependency = validated_data.get('dependency', instance.dependency)
        instance.save()

        return instance

    class Meta:
        model = Dependency
        fields = ['dependency']


class PosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pos
        fields = ['pos']


class TokenSerializer(serializers.ModelSerializer):

    lemma = EntrySerializer(required=False)
    pos = PosSerializer(required=False)
    features = MorphologicalAnnotationSerializer(many=True, required=False)
    syntax_annotations = SyntacticAnnotationSerializer(many=True, required=False)
    previous = serializers.PrimaryKeyRelatedField(queryset=Token.objects.all())

    def create(self, validated_data):
        lemma_data = validated_data.pop('lemma')
        pos_data = validated_data.pop('pos')
        features_data = validated_data.pop('features')
        syntax_annotations_data = validated_data.pop('syntax_annotations')
        previous_data = validated_data.pop('previous')

        token_instance = Token.objects.create(
            lemma=lemma_data, pos=pos_data, features=features_data, syntax_annotations=syntax_annotations_data, previous=previous_data, **validated_data)

        return token_instance

    def update(self, instance, validated_data):

        instance.lemma = validated_data.get('lemma', instance.lemma)
        instance.pos = validated_data.get('pos', instance.feature_value)
        instance.features = validated_data.get('features', instance.features)
        instance.syntax_annotations = validated_data.get('syntax_annotations', instance.syntax_annotations)
        instance.previous = validated_data.get('previous', instance.previous)

        instance.save()

        return instance

    class Meta:
        model = Token
        fields = ['transcription', 'transliteration', 'lemma', 'pos',
                  'features', 'syntax_annotations', 'comment', 'previous']
