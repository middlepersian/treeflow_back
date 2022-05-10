
from graphene import relay, String, Field, Boolean, ID, List, ObjectType, InputObjectType, Float
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Sentence, Text, Token
from mpcd.corpus.schemas.token import TokenInput
from mpcd.dict.models import Meaning
from mpcd.dict.schemas import MeaningInput

import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class SentenceNode(DjangoObjectType):
    class Meta:
        model = Sentence
        filter_fields = {
            'number': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'comment': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)


class SentenceInput(InputObjectType):
    id = ID(required=True)
    text = ID(required=True)
    number = Float(required=True)
    tokens = List(ID, required=True)
    translations = List(MeaningInput, required=True)
    comment = String()
    previous = ID()

# Query


class Query(ObjectType):
    sentence = relay.Node.Field(SentenceNode)
    all_sentences = DjangoFilterConnectionField(SentenceNode)

    @login_required
    def resolve_all_sentences(self, info, **kwargs):
        return gql_optimizer.query(Sentence.objects.all(), info)


# Mutations


class CreateSentence(relay.ClientIDMutation):

    success = Boolean()

    class Input:
        id = ID(required=True)
        text = ID(required=True)
        number = Float(required=True)
        tokens = List(ID, required=True)
        translations = List(MeaningInput, required=True)
        comment = String()
        previous = ID()

    errors = List(String)
    sentence = Field(SentenceNode)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):

        if Text.objects.filter(pk=from_global_id(input.get('text'))[1]).exists():
            text = Text.objects.get(pk=from_global_id(input.get('text'))[1])
            sentence_instance, sentence_created = Sentence.objects.get_or_create(text=text, number=input.get('number'))
        else:
            return cls(success=False, errors=['Wrong Text ID'])

        # add translations
        for translation_input in input.get('translations'):

            # check if translation exists, if not create it
            translation_instance, translation_created = Meaning.objects.get_or_create(
                meaning=translation_input.get('meaning'), language=translation_input.get('language'))

            # add translation to sentence
            sentence_instance.translations.add(translation_instance)

        # add tokens
        for token in input.get('tokens'):
            if Token.objects.filter(pk=from_global_id(token)[1]).exists():
                sentence_instance.tokens.add(Token.objects.get(pk=from_global_id(token)[1]))
            else:
                return cls(success=False, errors=['Wrong Token ID'])

        # check if previous is valid
        if input.get('previous', None):
            if Sentence.objects.filter(pk=from_global_id(input['previous'])[1]).exists():
                sentence_instance.previous = Sentence.objects.get(pk=from_global_id(input['previous'])[1])
            else:
                return cls(success=False, errors=['Wrong Previous ID'])

        if input.get('comment', None):
            sentence_instance.comment = input.get('comment')

        sentence_instance.save()
        return cls(sentence=sentence_instance, success=True)


class UpdateSentence(relay.ClientIDMutation):
    success = Boolean()

    class Input:
        id = ID(required=True)
        text = ID(required=True)
        number = Float(required=True)
        tokens = List(ID, required=True)
        translations = List(MeaningInput, required=True)
        comment = String()
        previous = ID()

    sentence = Field(SentenceNode)
    errors = List(String)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        # check if id is valid
        if Sentence.objects.filter(pk=from_global_id(input.get('id', None))[1]).exists():
            sentence_instance = Sentence.objects.get(pk=from_global_id(input.get('id', None))[1])
            if Text.objects.filter(pk=from_global_id(input.get('text', None))[1]).exists():
                sentence_instance.text = Text.objects.get(pk=from_global_id(input.get('text', None))[1])

            # clear tokens
            sentence_instance.tokens.clear()
            # update tokens
            for token in input.get('tokens'):
                token = Token.objects.get(pk=from_global_id(token.id)[1])
                sentence_instance.tokens.add(token)

            # clear translations
            sentence_instance.translations.clear()
            for translation_input in input.get('translations'):
                # check if translation exists, if not create it
                translation_instance, translation_created = Meaning.objects.get_or_create(
                    meaning=translation_input.get('meaning'), language=translation_input.get('language'))
                # add translation to sentence
                sentence_instance.translations.add(translation_instance)

            # update sentence number
            sentence_instance.number = input.get('number')

            if input.get('comment', None):
                sentence_instance.comment = input.get('comment')
              # check if previous is valid

            if input.get('previous', None):
                if Sentence.objects.filter(pk=from_global_id(input['previous'])[1]).exists():
                    sentence_instance.previous = Sentence.objects.get(pk=from_global_id(input['previous'])[1])
            elif not sentence_instance.previous and sentence_instance.number > 1.0:
                return cls(success=False, errors=['Wrong Previous ID'])

            sentence_instance.save()
            return cls(sentence=sentence_instance, success=True)

        else:
            return cls(success=False, errors=['Wrong ID'])


class DeleteSentence(relay.ClientIDMutation):

    class Input:
        id = ID(required=True)

    success = Boolean()
    sentence = Field(SentenceNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, id):
        if Sentence.objects.filter(pk=from_global_id(id)[1]).exists():
            sentence_instance = Sentence.objects.get(pk=from_global_id(id)[1])
            sentence_instance.delete()
            return cls(sentence=sentence_instance, success=True)

        else:
            return cls(success=False)


class AddTokensToSentence(relay.ClientIDMutation):

    class Input:
        id = ID(required=True)
        tokens = List(ID)

    success = Boolean()
    errors = List(String)
    sentence = Field(SentenceNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        if Sentence.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
            sentence_instance = Sentence.objects.get(pk=from_global_id(input.get('id', None))[1])
            if input.get('tokens', None) is not None:
                # clear up existing tokens
                sentence_instance.tokens.clear()
                for token_id in input.get('tokens', None):
                    if Token.objects.filter(pk=from_global_id(token_id)[1]).exists():
                        sentence_instance.tokens.add(Token.objects.get(pk=from_global_id(token_id)[1]))
                    else:
                        return cls(success=False, errors=['Wrong Token ID {}'.format(token_id)])
                sentence_instance.save()
                return cls(sentence=sentence_instance, success=True, errors=None)
        else:
            return cls(success=False, errors=['Wrong Sentence ID'])


class Mutation(ObjectType):
    create_sentence = CreateSentence.Field()
    update_sentence = UpdateSentence.Field()
    delete_sentence = DeleteSentence.Field()
    add_tokens_to_sentence = AddTokensToSentence.Field()
