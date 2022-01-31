
from graphene import relay, Token, String, Field, Boolean, ID, List, ObjectType, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Sentence, Text

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class SentenceNode(DjangoObjectType):
    class Meta:
        model = Sentence
        filter_fields = {'text': ['exact', 'icontains', 'istartswith'],
                         'translation': ['exact', 'icontains', 'istartswith'],
                         'comment': ['exact', 'icontains', 'istartswith']
                         }
        interfaces = (relay.Node,)


class SentenceInput(InputObjectType):
    text = String()
    tokens = List(Token)
    translation = String()
    comment = String()

# Query


class Query(ObjectType):
    sentence = relay.Node.Field(SentenceNode)
    all_sentences = DjangoFilterConnectionField(SentenceNode)

# Mutations


class CreateSentence(relay.ClientIDMutation):

    success = Boolean()

    class Input:
        id = ID()
        text = String()
        tokens = List(Token)
        translation = String()
        comment = String()

    sentence = Field(SentenceNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, text, tokens, translation, comment):
        logger.error('ROOT: {}'.format(root))
        # check that sentence does not exist same text and translation
        if Sentence.objects.filter(pk=from_global_id(id)[1]).exists():
            return cls(success=False)

        else:
            if Text.objects.filter(pk=from_global_id(text.id)[1]).exists():
                sentence_instance = Sentence.objects.create(translation=translation, text=text)
            else:
                return cls(success=False)
            if tokens:
                for token in tokens:
                    token = Token.objects.get(pk=from_global_id(token.id)[1])
                    sentence_instance.tokens.add(token)
            sentence_instance.comment = comment
            sentence_instance.save()
            return cls(sentence=sentence_instance, success=True)


class UpdateSentence(relay.ClientIDMutation):
    success = Boolean()

    class Input:
        id = ID(required=True)
        text = String()
        tokens = List(Token)
        translation = String()
        comment = String()

    sentence = Field(SentenceNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, text, tokens, translation, comment):
        if Sentence.objects.filter(pk=from_global_id(id)[1]).exists():
            sentence_instance = Sentence.objects.get(pk=from_global_id(id)[1])
            if Text.objects.filter(pk=from_global_id(text.id)[1]).exists():
                sentence_instance.text = Text.objects.get(pk=from_global_id(text.id)[1])
            if tokens:
                for token in tokens:
                    token = Token.objects.get(pk=from_global_id(token.id)[1])
                    sentence_instance.tokens.add(token)
            if translation:
                sentence_instance.translation = translation
            if comment:
                sentence_instance.comment = comment
            sentence_instance.save()
            return cls(sentence=sentence_instance, success=True)

        else:
            return cls(success=False)


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
