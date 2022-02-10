from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType, List
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
    identifier = String()
    codex = ID()


# Queries

class Query(ObjectType):
    folio = relay.Node.Field(FolioNode)
    all_folios = DjangoFilterConnectionField(FolioNode)


# Mutations


class CreateFolio(relay.ClientIDMutation):
    class Input:
        identifier = String(required=True)
        codex = ID()
        comment = String(required=False)
        previous = ID()

    folio = Field(FolioNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('CreateFolio.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))

        if input.get('identifier', None) is not None:
            identifier = input.get('identifier')
        else:
            return cls(success=False, errors=['identifier is required'])

        if input.get('codex', None) is not None:
            codex_instance = Codex.objects.get(pk=from_global_id(input.get('codex'))[1])
        else:
            return cls(success=False, errors=['codex is required'])

        if Folio.objects.filter(identifier=identifier).exists():
            return cls(success=False, errors=['Folio already exists'])

        folio = Folio.objects.create(identifier=identifier, codex=codex_instance)

        if input.get('comment', None) is not None:
            folio.comment = input.get('comment')

        if input.get('previous', None) is not None:
            if Folio.objects.filter(pk=from_global_id(input['previous'])[1]).exists():
                folio.previous = Folio.objects.get(pk=from_global_id(input['previous'])[1])

        folio.save()

        return cls(folio=folio, success=True)


class UpdateFolio(relay.ClientIDMutation):
    class Input:
        id = ID()
        identifier = String(required=True)
        codex = CodexInput()
        comment = String(required=False)
        previous = FolioInput()

    folio = Field(FolioNode)
    success = Boolean()

    @ classmethod
    def mutate_and_get_payload(cls, root, info, id, identifier, codex, comment):
        logger.debug('UpdateFolio.mutate_and_get_payload()')
        if Folio.objects.filter(pk=from_global_id(id)[1]).exists() and Codex.objects.filter(pk=from_global_id(codex.id)[1]).exists():
            folio_instance = Folio.objects.get(id=id)
            folio_instance.identifier = identifier
            folio_instance.comment = comment
            folio_instance.codex = Codex.objects.get(pk=from_global_id(codex.id)[1])
            folio_instance.comment = comment
            if input.get('previous', None) is not None:
                if Folio.objects.filter(pk=from_global_id(input['previous']['id'])[1]).exists():
                    folio_instance.previous = Folio.objects.get(pk=from_global_id(input['previous']['id'])[1])
            folio_instance.save()
            return cls(folio=folio_instance, success=True)
        else:
            return cls(success=False)


class DeleteFolio(relay.ClientIDMutation):
    class Input:
        id = ID()

    success = Boolean()

    @ classmethod
    def mutate_and_get_payload(cls, root, info, id):
        logger.debug('DeleteFolio.mutate_and_get_payload()')
        if Folio.objects.filter(pk=from_global_id(id)[1]).exists():
            folio_instance = Folio.objects.get(pk=from_global_id(id)[1])
            folio_instance.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_folio = CreateFolio.Field()
    update_folio = UpdateFolio.Field()
    delete_folio = DeleteFolio.Field()
