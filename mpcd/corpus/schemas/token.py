
from graphene import relay, ObjectType, String, Field, ID, Boolean, List, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.dict.models import Entry, Lemma, Language, Translation
from mpcd.corpus.models import Token, Feature, FeatureValue, MorphologicalAnnotation, POS, Dependency, Text
from mpcd.corpus.schemas.morphological_annotation import MorphologicalAnnotationInput
from mpcd.corpus.schemas.pos import POSInput
from mpcd.corpus.schemas.dependency import DependencyInput
from mpcd.corpus.schemas.text import TextInput
from mpcd.dict.schemas.entry import EntryInput
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
    id = ID()
    transcription = String()
    transliteration = String()
    text = TextInput()
    language = String()
    lemma = EntryInput()
    pos = POSInput()
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
        text = ID()
        language = ID()
        lemma = EntryInput()
        pos = POSInput()
        morphological_annotation = List(MorphologicalAnnotationInput)
        syntactic_annotation = List(DependencyInput)
        comment = String()
        avestan = String()
        previous = TokenInput()

    token = Field(TokenNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if input.get('transcription', None) is None and input.get('transliteration', None) is None:
            return cls(token=None, success=False, errors=["No transcription or transliteration provided"])
        else:
            token = Token.objects.create(
                transcription=input['transcription'], transliteration=input['transliteration'])

        # check if text available
        if input.get('text', None) is not None:
            if Text.objects.filter(pk=from_global_id(input['text'])[1]).exists():
                text = Text.objects.get(pk=from_global_id(input['text'])[1])
                token.text = text
            else:
                return cls(token=None, success=False, errors=["Text with ID {} not found".format(input['text'])])

        # check if language available
        if input.get('language', None) is not None:
            token.language = input.get('language', None)

        # check if lemma available
        # TODO complex version of entry here
        if input.get('lemma', None) is not None:

            # get lemmas word
            if input.get('lemma').get('word', None) is not None:
                lemma_word = input.get('lemma').get('word')
                if input.get('lemma').get('language') is not None:
                    lemma_lang = input.get('lemma').get('language')

                    lemma, lemma_created = Lemma.objects.get_or_create(word=lemma_word, language=lemma_lang)

                else:
                    return cls(token=None, success=False, errors=["No language provided for lemma"])

            else:
                return cls(token=None, success=False, errors=["No lemma word provided"])

            if lemma:
                entry = Entry.objects.create(lemma=lemma)

            # check if translations available
            if input.get('lemma').get('translations') is not None:
                for translation in input['lemma']['translations']:
                    # check if language in mutation input is available
                    translation_obj, translation_obj_created = Translation.objects.get_or_create(
                        word=translation['word'], language=translation['language'])
                    entry.translations.add(translation_obj)

            # add the entry to the token
            token.lemma = entry

        # check if pos available
        if input.get('pos', None) is not None:
            # check if pos with same name already exists
            pos, pos_created = POS.objects.get_or_create(identifier=input['pos']['identifier'])
            token.pos = pos
        # check if morphological annotation available
        if input.get('morphological_annotation', None) is not None:
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
        if input.get('syntactic_annotation') is not None:
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
        if input.get('comment', None) is not None:
            token.comment = input['comment']
        # check if avestan available
        if input.get('avestan', None) is not None:
            token.avestan = input['avestan']
        # check if previous token available
        if input.get('previous', None) is not None:
            # check if previous token with assigned id already exists
            if Token.objects.filter(pk=from_global_id(input['previous'])[1]).exists():
                token.previous = Token.objects.filter(pk=from_global_id(input['previous'])[1]).first()
            else:
                return cls(token=None, success=False, errors=["Previous token with ID {} not found".format(input['previous'])])


class UpdateToken(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        transcription = String(required=False)
        transliteration = String(required=False)
        lemma = String(required=False)
        pos = String(required=False)
        morphological_annotation = List(String, required=False)
        syntactic_annotation = List(String, required=False)
        comment = String(required=False)
        avestan = String(required=False)
        previous = String(required=False)

    token = Field(TokenNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if input.get('id', None) is not None:
            # check if token with assigned id already exists
            if Token.objects.filter(pk=from_global_id(input['id'])[1]).exists():
                # get the token
                token = Token.objects.get(pk=from_global_id(input['id'])[1])
            else:
                return cls(token=None, success=False, errors=["Token with ID {} not found".format(input['id'])])

            # check if transcription available
            if input.get('transcription', None) is not None:
                token.transcription = input['transcription']
            # check if transliteration available
            if input.get('transliteration', None) is not None:
                token.transliteration = input['transliteration']
            # check if lemma available
            # check if language available
        if input.get('language', None) is not None:
            token.language = input.get('language', None)

        # check if lemma available
        if input.get('lemma', None) is not None:

            # get lemmas word
            if input.get('lemma').get('word', None) is not None:
                lemma_word = input.get('lemma').get('word')
                if input.get('lemma').get('language') is not None:
                    lemma_lang = input.get('lemma').get('language')

                    lemma, lemma_created = Lemma.objects.get_or_create(word=lemma_word, language=lemma_lang)

                else:
                    return cls(token=None, success=False, errors=["No language provided for lemma"])

            else:
                return cls(token=None, success=False, errors=["No lemma word provided"])

            if lemma:
                entry = Entry.objects.create(lemma=lemma)

            # check if translations available
            if input.get('lemma').get('translations') is not None:
                for translation in input['lemma']['translations']:
                    # check if language in mutation input is available
                    translation_obj, translation_obj_created = Translation.objects.get_or_create(
                        word=translation['word'], language=translation['language'])
                    entry.translations.add(translation_obj)

            # add the entry to the token
            token.lemma = entry

        # check if language available
        if input.get('language', None) is not None:
            token.language = input.get('language', None)

            # check if pos available
        if input.get('pos', None) is not None:
            # check if pos with same name already exists
            pos, pos_created = POS.objects.get_or_create(identifier=input['pos']['identifier'])
            token.pos = pos
        # check if morphological annotation available
        if input.get('morphological_annotation', None) is not None:
            token.morphological_annotations.clear()
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
        if input.get('syntactic_annotation') is not None:
            token.syntactic_annotations.clear()
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
        if input.get('comment', None) is not None:
            token.comment = input['comment']
        # check if avestan available
        if input.get('avestan', None) is not None:
            token.avestan = input['avestan']
        # check if previous token available
        if input.get('previous', None) is not None:
            # check if previous token with assigned id already exists
            if Token.objects.filter(pk=from_global_id(input['previous']['id'])[1]).exists():
                token.previous = Token.objects.filter(pk=from_global_id(input['previous']['id'])[1]).first()
        # save token
        token.save()
        return cls(token=token, success=True)


class DeleteToken(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        if Token.objects.filter(pk=from_global_id(id)[1]).exists():
            token_instance = Token.objects.get(pk=from_global_id(id)[1])
            token_instance.delete()
            return cls(success=True)

        else:
            return cls(success=False)


class JoinTokens(relay.ClientIDMutation):
    class Input():
        token = ID()
        previous = ID()

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # get token
        token = Token.objects.get(pk=from_global_id(input['token'])[1])
        logger.error("TOKEN_ID: {}".format(token))
        # get previous token
        previous = Token.objects.get(pk=from_global_id(input['previous'])[1])
        logger.error("PREVIOUS_TOKEN_ID: {}".format(previous))
        # join tokens
        token.previous = previous
        previous.save()
        token.save()
        return cls(success=True)


class Mutation(ObjectType):
    create_token = CreateToken.Field()
    delete_token = DeleteToken.Field()
    join_tokens = JoinTokens.Field()
