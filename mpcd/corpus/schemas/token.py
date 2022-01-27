from operator import indexOf
from graphene import relay, ObjectType, String, Field, ID, Boolean, List, Int, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.dict.models import Entry, Lemma, Language, Translation
from mpcd.corpus.models import Token, Feature, FeatureValue, MorphologicalAnnotation, Pos, Dependency
from mpcd.corpus.schemas import MorphologicalAnnotationNode, MorphologicalAnnotationInput
from mpcd.corpus.schemas import PosNode, PosInput
from mpcd.corpus.schemas import DependencyNode, DependencyInput
from mpcd.dict.schemas import EntryNode, EntryInput
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class TokenNode(DjangoObjectType):
    class Meta:
        model = Token
        filter_fields = {'transcription': ['exact', 'icontains', 'istartswith'],
                         'transliteration': ['exact', 'icontains', 'istartswith']
                         }
        interfaces = (relay.Node,)


class TokenInput(InputObjectType):
    transcription = String()
    transliteration = String()
    lemma = EntryInput()
    pos = PosInput()
    morphological_annotation = List(MorphologicalAnnotationInput)
    syntactic_annotation = List(DependencyInput)
    comment = String()
    avestan = String()
    previous = TokenNode()

# Queries


class Query(ObjectType):
    token = relay.Node.Field(TokenNode)
    all_tokens = DjangoFilterConnectionField(TokenNode)

# Mutations


class CreateToken(relay.ClientIDMutation):
    class Input:
        transcription = String()
        transliteration = String()
        lemma = EntryInput()
        pos = PosInput()
        morphological_annotation = List(MorphologicalAnnotationInput)
        syntactic_annotation = List(DependencyInput)
        comment = String()
        avestan = String()
        previous = TokenNode()

    token = Field(TokenNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # check if token wiht same ID already exists
        if Token.objects.filter(id=input['id']).exists():
            return cls(success=False)
        # create token
        else:
            # add transcription and transliteration
            token = Token.objects.create(transcription=input['transcription'], transliteration=input['transliteration'])
            # check if lemma available
            if input['lemma']:
                # check if language in mutation input is available
                if input['lemma']['language']['identifier']:
                    # check if lemma with same word and language already exists
                    if Lemma.objects.filter(word=input['lemma']['word']).select_related('language').filter(identifier=input['lemma']['word']['language']['identifier']).exists():
                        lemma = Lemma.objects.filter(word=input['lemma']['word']).select_related(
                            'language').filter(identifier=input['lemma']['word']['language']['identifier'])[0]

                    else:
                        # get the language
                        lang, lang_created = Language.objects.get_or_create(
                            identifier=input['lemma']['word']['language']['identifier'])

                        if lang_created:
                            # create the lemma
                            lemma = Lemma.objects.create(word=input['lemma']['word'], language=lang)
                            token.lemma = lemma

            # check if pos available
            if input['pos']:
                # check if pos with same name already exists
                pos = Pos.objects.get_or_create(pos=input['pos']['pos'])
                token.pos = pos
            # check if morphological annotation available
            if input['morphological_annotation']:
                for annotation in input['morphological_annotation']:
                    # check if annotation with same feature and feature value already exists
                    if MorphologicalAnnotation.objects.select_related('feature').filter(identifier=annotation['feature']['identifier']).select_related('feature_value').filter(identifier=annotation['feature_value']['identifier']).exists():
                        annotation_obj = MorphologicalAnnotation.objects.select_related('feature').filter(identifier=annotation['feature']['identifier']).select_related(
                            'feature_value').filter(identifier=annotation['feature_value']['identifier']).first()
                    else:
                        # create the annotation
                        feature, feature_created = Feature.objects.get_or_create(
                            identifier=annotation['feature']['identifier'])
                        feature_value, feature_value_created = FeatureValue.objects.get_or_create(
                            identifier=annotation['feature_value']['identifier'])
                        annotation_obj = MorphologicalAnnotation.objects.create(
                            feature=feature, feature_value=feature_value)

                    token.morphological_annotations.add(annotation_obj)
            # check if syntactic annotation available
            if input['syntactic_annotation']:
                for annotation in input['syntactic_annotation']:
                    # check if dependency with same head and rel already exists
                    if Dependency.objects.filter(head=annotation['head']).filter(rel=annotation['rel']).exists():
                        annotation_obj = Dependency.objects.filter(
                            head=annotation['head']).filter(rel=annotation['rel']).first()
                    else:
                        # create the annotation
                        annotation_obj = Dependency.objects.create(
                            head=annotation['head'], rel=annotation['rel'])
                    token.syntactic_annotations.add(annotation_obj)
            # check if comment available
            if input['comment']:
                token.comment = input['comment']
            # check if avestan available
            if input['avestan']:
                token.avestan = input['avestan']
            # check if previous token available
            if input['previous']:
                # check if previous token with assigned id already exists
                if Token.objects.filter(id=input['previous']['id']).exists():
                    token.previous = Token.objects.filter(id=input['previous']['id']).first()
            # save token
            token.save()
            return cls(token=token, success=True)


class Mutation(ObjectType):
    create_token = CreateToken.Field()
