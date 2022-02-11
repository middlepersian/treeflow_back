
from graphene import relay, ObjectType, String, Field, ID, Boolean, List, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.dict.models import Entry, Lemma, Language, Translation
from mpcd.corpus.models import Token, Feature, FeatureValue, MorphologicalAnnotation, POS, Dependency, Text
from mpcd.corpus.schemas import MorphologicalAnnotationInput
from mpcd.corpus.schemas import POSInput
from mpcd.corpus.schemas import DependencyInput
from mpcd.corpus.schemas import TextInput
from mpcd.dict.schemas import EntryInput
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
        logger.error("INPUT: {}".format(input))
        # check if input has an ID
        # TODO check if relay generates a new ID .btw check if section.py does it better
        if input.get('id', None) is None:
            # add transcription and transliteration
            token = Token.objects.create(transcription=input['transcription'], transliteration=input['transliteration'])
            logger.error("TOKEN: {}".format(token))

            if input.get('text', None) is not None:
                if Text.objects.filter(pk=from_global_id(input['text'])[1]).exists():
                    text = Text.objects.get(pk=from_global_id(input['text'])[1])
                    token.text = text
                else:
                    return cls(token=None, success=False)

            # check if language available
            if input.get('language', None) is not None:
                if Language.objects.filter(pk=from_global_id(input['language'])[1]).exists():
                    language = Language.objects.get(pk=from_global_id(input['language'])[1])
                    token.language = language

            # check if lemma available
            if input.get('lemma', None) is not None:

                # check if language in mutation input is available
                if input['lemma']['language']['identifier']:
                    # check if lemma with same word and language already exists
                    if Lemma.objects.filter(word=input['lemma']['word']).select_related('language').filter(identifier=input['lemma']['language']['identifier']).exists():
                        lemma = Lemma.objects.filter(word=input['lemma']['word']).select_related(
                            'language').filter(identifier=input['lemma']['word']['language']['identifier'])[0]

                    else:
                        # get the language
                        lang, lang_created = Language.objects.get_or_create(
                            identifier=input['lemma']['word']['language']['identifier'])

                        if lang_created:
                            # create the lemma
                            lemma = Lemma.objects.create(word=input['lemma']['word'], language=lang)
                            # create the entry
                    if lemma:
                        entry = Entry.objects.create(lemma=lemma)
                    # check if translation available
                    if input.get('lemma').get('translations') is not None:
                        for translation in input['lemma']['translations']:
                            # check if language in mutation input is available
                            if translation['language']['identifier']:
                                # check if translation with same word and language already exists
                                if Translation.objects.filter(word=translation['word']).select_related('language').filter(identifier=translation['language']['identifier']).exists():
                                    translation_obj = Translation.objects.filter(word=translation['word']).select_related(
                                        'language').filter(identifier=translation['language']['identifier'])[0]
                                else:
                                    # get the language
                                    lang, lang_created = Language.objects.get_or_create(
                                        identifier=translation['language']['identifier'])

                                    if lang_created:
                                        # create the translation
                                        translation_obj = Translation.objects.create(
                                            word=translation['word'], language=lang)

                                # create the translation
                                if translation_obj:
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
                # check if previous token with assigned id does not exist
                if not Token.objects.filter(pk=from_global_id(input['previous']['id'])[1]).exists():
                    # assign previous token
                    token.previous = Token.objects.get(pk=from_global_id(input['previous']['id'])[1])
            # save token
            token.save()
            return cls(token=token, success=True)

        else:
            return cls(token=None, success=False)


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
        logger.error("INPUT: {}".format(input))
        # check if input has an ID
        # TODO check if relay generates a new ID .btw check if section.py does it better
        if input.get('id', None) is not None:
            # get the token
            token = Token.objects.get(pk=from_global_id(input['id'])[1])
            # check if transcription available
            if input.get('transcription', None) is not None:
                token.transcription = input['transcription']
            # check if transliteration available
            if input.get('transliteration', None) is not None:
                token.transliteration = input['transliteration']
            # check if lemma available
              # check if lemma available
            if input.get('lemma', None) is not None:

                # check if language in mutation input is available
                if input['lemma']['language']['identifier']:
                    # check if lemma with same word and language already exists
                    if Lemma.objects.filter(word=input['lemma']['word']).select_related('language').filter(identifier=input['lemma']['language']['identifier']).exists():
                        lemma = Lemma.objects.filter(word=input['lemma']['word']).select_related(
                            'language').filter(identifier=input['lemma']['word']['language']['identifier'])[0]

                    else:
                        # get the language
                        lang, lang_created = Language.objects.get_or_create(
                            identifier=input['lemma']['word']['language']['identifier'])

                        if lang_created:
                            # create the lemma
                            lemma = Lemma.objects.create(word=input['lemma']['word'], language=lang)
                            # create the entry
                    if lemma:
                        entry = Entry.objects.create(lemma=lemma)
                    # check if translation available
                    if input.get('lemma').get('translations', None) is not None:
                        token.lemma.translations.clear()
                        for translation in input['lemma']['translations']:
                            # check if language in mutation input is available
                            if translation['language']['identifier']:
                                # check if translation with same word and language already exists
                                if Translation.objects.filter(word=translation['word']).select_related('language').filter(identifier=translation['language']['identifier']).exists():
                                    translation_obj = Translation.objects.filter(word=translation['word']).select_related(
                                        'language').filter(identifier=translation['language']['identifier'])[0]
                                else:
                                    # get the language
                                    lang, lang_created = Language.objects.get_or_create(
                                        identifier=translation['language']['identifier'])

                                    if lang_created:
                                        # create the translation
                                        translation_obj = Translation.objects.create(
                                            word=translation['word'], language=lang)

                                # create the translation
                                if translation_obj:
                                    entry.translations.add(translation_obj)

                    # add the entry to the token
                    token.lemma = entry

            # check if language available
            if input.get('language', None) is not None:
                if Language.objects.filter(pk=from_global_id(input['language'])[1]).exists():
                    language = Language.objects.get(pk=from_global_id(input['language'])[1])
                    token.language = language

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
                # check if previous token with assigned id does not exist
                if not Token.objects.filter(pk=from_global_id(input['previous']['id'])[1]).exists():
                    # assign previous token
                    token.previous = Token.objects.get(pk=from_global_id(input['previous']['id'])[1])
            # save token
            token.save()
            return cls(token=token, success=True)

        else:
            return cls(token=None, success=False)


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
