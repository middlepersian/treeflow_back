from graphene import relay, InputObjectType, String, Field, ObjectType, List, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.corpus.models import Sigle


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class SigleNode(DjangoObjectType):
    class Meta:
        model = Sigle
        filter_fields = {'sigle': ['exact', 'icontains', 'istartswith'],
                         'genre': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class SigleInput(InputObjectType):
    id = ID()
    sigle = String()
    genre = String()


class Query(ObjectType):
    sigle = relay.Node.Field(SigleNode)
    all_sigle = DjangoFilterConnectionField(SigleNode)


# Mutations

class CreateSigle(relay.ClientIDMutation):
    class Input:
        sigle = String()
        genre = String()

    sigle = Field(SigleNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, sigle, genre):

        if Sigle.objects.filter(sigle=sigle, genre=genre).exists():
            return cls(success=False)
        else:
            sigle = Sigle.objects.create(sigle=sigle, genre=genre)
            return cls(sigle=sigle, success=True)


class UpdateSigle(relay.ClientIDMutation):
    class Input:
        id = ID()
        sigle = String()
        genre = String()

    sigle = Field(SigleNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, sigle, genre):

        if Sigle.objects.filter(id=id).exists():
            sigle = Sigle.objects.get(id=id)
            sigle.sigle = sigle
            sigle.genre = genre
            sigle.save()
            return cls(sigle=sigle, success=True)
        else:
            return cls(success=False)


class DeleteSigle(relay.ClientIDMutation):
    class Input:
        id = ID()

    sigle = Field(SigleNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):

        if Sigle.objects.filter(id=id).exists():
            sigle = Sigle.objects.get(id=id)
            sigle.delete()
            return cls(sigle=sigle, success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_sigle = CreateSigle.Field()
    update_sigle = UpdateSigle.Field()
    delete_sigle = DeleteSigle.Field()
