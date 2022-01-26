from graphene import relay, InputObjectType, String, Field, ObjectType, List, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.corpus.models import TextSigle


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class TextSigleNode(DjangoObjectType):
    class Meta:
        model = TextSigle
        filter_fields = {'sigle': ['exact', 'icontains', 'istartswith'],
                         'genre': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class TextSigleInput(InputObjectType):
    sigle = String()
    genre = String()


class Query(ObjectType):
    sigle = relay.Node.Field(TextSigleNode)
    all_sigle = DjangoFilterConnectionField(TextSigleNode)


# Mutations

class CreateTextSigle(relay.ClientIDMutation):
    class Input:
        sigle = String()
        genre = String()

    sigle = Field(TextSigleNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, sigle, genre):

        if TextSigle.objects.filter(sigle=sigle, genre=genre).exists():
            return cls(success=False)
        else:
            sigle = TextSigle.objects.create(sigle=sigle, genre=genre)
            return cls(sigle=sigle, success=True)


class UpdateTextSigle(relay.ClientIDMutation):
    class Input:
        id = ID()
        sigle = String()
        genre = String()

    sigle = Field(TextSigleNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, sigle, genre):

        if TextSigle.objects.filter(id=id).exists():
            sigle = TextSigle.objects.get(id=id)
            sigle.sigle = sigle
            sigle.genre = genre
            sigle.save()
            return cls(sigle=sigle, success=True)
        else:
            return cls(success=False)


class DeleteTextSigle(relay.ClientIDMutation):
    class Input:
        id = ID()

    sigle = Field(TextSigleNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):

        if TextSigle.objects.filter(id=id).exists():
            sigle = TextSigle.objects.get(id=id)
            sigle.delete()
            return cls(sigle=sigle, success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_text_sigle = CreateTextSigle.Field()
    update_text_sigle = UpdateTextSigle.Field()
    delete_text_sigle = DeleteTextSigle.Field()
