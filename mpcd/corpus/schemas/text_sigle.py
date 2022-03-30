from graphene import relay, InputObjectType, String, Field, ObjectType, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

from mpcd.corpus.models import TextSigle

import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


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
    text_sigle = relay.Node.Field(TextSigleNode)
    all_text_sigles = DjangoFilterConnectionField(TextSigleNode)

    @login_required
    def resolve_all_text_sigles(self, info, **kwargs):
        return gql_optimizer.query(TextSigle.objects.all(), info)


# Mutations

class CreateTextSigle(relay.ClientIDMutation):
    class Input:
        sigle = String()
        genre = String()

    sigle = Field(TextSigleNode)
    success = Boolean()

    @classmethod
    @login_required

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
    @login_required

    def mutate_and_get_payload(cls, root, info, id, sigle, genre):

        if TextSigle.objects.filter(pk=from_global_id(id)[1]).exists():
            sigle = TextSigle.objects.get(pk=from_global_id(id)[1])
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
    @login_required

    def mutate_and_get_payload(cls, root, info, id):

        if TextSigle.objects.filter(pk=from_global_id(id)[1]).exists():
            sigle = TextSigle.objects.get(pk=from_global_id(id)[1])
            sigle.delete()
            return cls(sigle=sigle, success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_text_sigle = CreateTextSigle.Field()
    update_text_sigle = UpdateTextSigle.Field()
    delete_text_sigle = DeleteTextSigle.Field()
