
from graphene import relay, String, Field, Boolean, ID, List, ObjectType, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Sentence, Text, Token
from mpcd.corpus.schemas.token import TokenNode
from mpcd.dict.models import Language, Translation
from mpcd.dict.schemas.translation import TranslationInput

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class SentenceNode(DjangoObjectType):
    class Meta:
        model = Sentence
        filter_fields = {
            'comment': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)


class SentenceInput(InputObjectType):
    text = String()
    tokens = List(TokenNode)
    translation = List(TranslationInput)
    comment = String()

# Query


class Query(ObjectType):
    sentence = relay.Node.Field(SentenceNode)
    all_sentences = DjangoFilterConnectionField(SentenceNode)

# Mutations


class CreateSentence(relay.ClientIDMutation):

    success = Boolean()

    class Input:
        text = ID()
        tokens = List(TokenNode)
        translations = List(TranslationInput)
        comment = String()

    sentence = Field(SentenceNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        logger.error('ROOT: {}'.format(root))
        if input.get('text', None) is not None:
            if Text.objects.filter(pk=from_global_id('text')[1]).exists():
                text = Text.objects.get(pk=from_global_id(input.get('text'))[1])
                sentence_instance = Sentence.objects.create(text=text)
            else:
                return cls(success=False, errors=['Wrong Text ID'])

        else:
            return cls(success=False, errors=['Text ID is required'])

        if input.get('comment', None) is not None:
            sentence_instance.comment = input.get('comment')

        if input.get('translations', None) is not None:
            for translation_input in input.get('translations'):
                # check if language exists
                if Language.objects.filter(identifier=translation_input.get('language').get('identifier')).exists():
                    language_instance = Language.objects.get(
                        identifier=translation_input.get('language').get('identifier'))

                    # check if translation exists, if not create it
                    translation_instance, translation_created = Translation.objects.get_or_create(
                        text=translation_input.get('text'), language=language_instance)

                    # add translation to sentence
                    sentence_instance.translations.add(translation_instance)

                else:
                    return cls(success=False, errors=['Wrong Language ID'])

        # add tokens
        if input.get('tokens', None) is not None:
            for token in input.get('tokens'):
                if Token.objects.filter(pk=from_global_id(token)[1]).exists():
                    sentence_instance.tokens.add(Token.objects.get(pk=from_global_id(token)[1]))
                else:
                    return cls(success=False, errors=['Wrong Token ID'])

        # check if previous is valid
        if input.get('previous', None) is not None:
            if not Sentence.objects.filter(pk=from_global_id(input['previous'])[1]).exists():
                sentence_instance.previous = Sentence.objects.get(pk=from_global_id(input['previous'])[1])
            else:
                return cls(success=False, errors=['Wrong Previous ID'])

        sentence_instance.save()
        return cls(sentence=sentence_instance, success=True)


class UpdateSentence(relay.ClientIDMutation):
    success = Boolean()

    class Input:
        id = ID(required=True)
        text = ID()
        tokens = List(TokenNode)
        translations = List(TranslationInput)
        comment = String()

    sentence = Field(SentenceNode)
    errors = List(String)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # check if id is valid
        if Sentence.objects.filter(pk=from_global_id(input.get('id', None))[1]).exists():
            sentence_instance = Sentence.objects.get(pk=from_global_id(id)[1])
            if Text.objects.filter(pk=from_global_id(input.get('text', None))[1]).exists():
                sentence_instance.text = Text.objects.get(pk=from_global_id(text.id)[1])
            if input.get('tokens', None) is not None:
                sentence_instance.tokens.clear()
                for token in input.get('tokens', None):
                    token = Token.objects.get(pk=from_global_id(token.id)[1])
                    sentence_instance.tokens.add(token)
            if input.get('translations', None) is not None:
                sentence_instance.translations.clear()
                for translation_input in input.get('translations'):
                    # check if language exists
                    if Language.objects.filter(identifier=translation_input.get('language').get('identifier')).exists():
                        language_instance = Language.objects.get(
                            identifier=translation_input.get('language').get('identifier'))

                        # check if translation exists, if not create it
                        translation_instance, translation_created = Translation.objects.get_or_create(
                            text=translation_input.get('text'), language=language_instance)

                        # add translation to sentence
                        sentence_instance.translations.add(translation_instance)

                else:
                    return cls(success=False, errors=['Wrong Language ID'])

            if input.get('comment', None) is not None:
                sentence_instance.comment = input.get('comment')

            sentence_instance.save()
            return cls(sentence=sentence_instance, success=True)

        else:
            return cls(success=False, errors=['Wrong ID'])


class DeleteSentence(relay.ClientIDMutation):
    success = Boolean()

    class Input:
        id = ID(required=True)

    sentence = Field(SentenceNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        if Sentence.objects.filter(pk=from_global_id(id)[1]).exists():
            sentence_instance = Sentence.objects.get(pk=from_global_id(id)[1])
            sentence_instance.delete()
            return cls(sentence=sentence_instance, success=True)

        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_sentence = CreateSentence.Field()
    update_sentence = UpdateSentence.Field()
    delete_sentence = DeleteSentence.Field()
