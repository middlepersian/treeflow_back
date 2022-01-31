from calendar import c
from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Codex, Folio
from mpcd.corpus.schemas.codex import CodexInput, CodexNode


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class FolioNode(DjangoObjectType):

    class Meta:
        model = Folio
        filter_fields = {'identifier': ['exact', 'icontains', 'istartswith'],
                         'comment': ['exact', 'icontains', 'istartswith']}

        interfaces = (relay.Node, )


class FolioInput(InputObjectType):
    id = ID()
    identifier = String(required=True)
    codex = CodexInput(required=True)
    comment = String(required=False)


class Query(ObjectType):
    folio = relay.Node.Field(FolioNode)
    all_folios = DjangoFilterConnectionField(FolioNode)

# Mutations


class CreateFolio(relay.ClientIDMutation):
    class Input:
        identifier = String(required=True)
        codex = CodexInput()
        comment = String(required=False)

    folio = Field(FolioNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, identifier, codex, comment):
        logger.debug('CreateFolio.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))
        if Folio.objects.filter(identifier=identifier).exists():
            return cls(success=False)
        else:
            folio_instance = Folio.objects.create()
            folio_instance.identifier = identifier
            folio_instance.codex = codex
            folio_instance.comment = comment
            folio_instance.save()
            return cls(folio=folio_instance, success=True)


class UpdateFolio(relay.ClientIDMutation):
    class Input:
        id = ID()
        identifier = String(required=True)
        codex = CodexInput()
        comment = String(required=False)

    folio = Field(FolioNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, identifier, codex, comment):
        logger.debug('UpdateFolio.mutate_and_get_payload()')
        if Folio.objects.filter(pk=from_global_id(id)[1]).exists() and Codex.objects.filter(pk=from_global_id(codex.id)[1]).exists():
            folio_instance = Folio.objects.get(id=id)
            folio_instance.identifier = identifier
            folio_instance.comment = comment
            folio_instance.codex = Codex.objects.get(id=codex.id)
            folio_instance.comment = comment
            folio_instance.save()
            return cls(folio=folio_instance, success=True)
        else:
            return cls(success=False)


class DeleteFolio(relay.ClientIDMutation):
    class Input:
        id = ID()

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        logger.debug('DeleteFolio.mutate_and_get_payload()')
        if Folio.objects.filter(pk=from_global_id(id)[1]).exists():
            folio_instance = Folio.objects.get(pk=from_global_id(id)[1])
            folio_instance.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_author = CreateFolio.Field()
    update_author = UpdateFolio.Field()
    delete_author = DeleteFolio.Field()
