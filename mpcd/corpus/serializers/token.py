from rest_framework import serializers
from .. models import FeatureValue, Feature, MorphologicalAnnotation, Dependency, POS, Token
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
        model = Dependency
        fields = ['head', 'rel']


class POSSerializer(serializers.ModelSerializer):
    class Meta:
        model = POS
        fields = ['identifier']


class TokenSerializer(serializers.ModelSerializer):

    lemma = EntrySerializer(required=False)
    pos = POSSerializer(required=False)
    morphological_annotation = MorphologicalAnnotationSerializer(many=True, required=False)
    syntactic_annotation = DependencySerializer(many=True, required=False)
    previous = serializers.PrimaryKeyRelatedField(queryset=Token.objects.all(), required=False, allow_null=True)

    def create(self, validated_data):
        lemma_data = validated_data.pop('lemma')
        pos_data = validated_data.pop('pos')
        syntactic_annotation_data = validated_data.pop('syntactic_annotation')
        morphological_annotation_data = validated_data.pop('morphological_annotation')
        previous_data = validated_data.pop('previous')

        token_instance = Token.objects.create(
            lemma=lemma_data, pos=pos_data, syntactic_annotation=syntactic_annotation_data, morphological_annotation=morphological_annotation_data, previous=previous_data, **validated_data)

        return token_instance

    def update(self, instance, validated_data):

        instance.lemma = validated_data.get('lemma', instance.lemma)
        instance.pos = validated_data.get('pos', instance.feature_value)
        instance.syntactic_annotation = validated_data.get('syntactic_annotation', instance.syntactic_annotation)
        instance.morphological_annotation = validated_data.get(
            'morphological_annotation', instance.morphological_annotation)
        instance.previous = validated_data.get('previous', instance.previous)

        instance.save()

        return instance

    class Meta:
        model = Token
        fields = ['transcription', 'transliteration', 'lemma', 'pos',
                  'morphological_annotation', 'syntactic_annotation', 'comment', 'previous']
