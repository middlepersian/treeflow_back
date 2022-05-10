from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import BibEntry, Facsimile, CodexPart

import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required, superuser_required


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class FacsimileNode(DjangoObjectType):

    class Meta:
        model = Facsimile
        filter_fields = {'bib_entry': ['exact'], }
        interfaces = (relay.Node, )


class FacsimileInput(InputObjectType):
    bib_entry = ID(required=True)
    codex_part = ID(required=True)

# Queries


class Query(ObjectType):
    facsimile = relay.Node.Field(FacsimileNode)
    all_facsimiles = DjangoFilterConnectionField(FacsimileNode)

    @login_required
    def resolve_all_facsimiles(self, info, **kwargs):
        return gql_optimizer.query(Facsimile.objects.all(), info)


# Mutations

class CreateFacsimile(relay.ClientIDMutation):
    class Input:
        bib_entry = ID(required=True)
        codex_part = ID(required=True)

    facsimile = Field(FacsimileNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('CreateFacsimile.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))

        if BibEntry.objects.filter(pk=from_global_id(input.get('bib_entry'))[1]).exists():
            bib_entry = BibEntry.objects.get(pk=from_global_id(input.get('bib_entry'))[1])
            facsimile_instance, facsimile_created = Facsimile.objects.get_or_create(bib_entry=bib_entry)
        else:
            return cls(success=False, errors=['bib_entry ID does not exist'])

        if CodexPart.objects.filter(pk=from_global_id(input.get('codex_part'))[1]).exists():
            codex_part = CodexPart.objects.get(pk=from_global_id(input.get('codex_part'))[1])
            facsimile_instance.codex_part = codex_part
            facsimile_instance.save()

        else:
            return cls(success=False, errors=['codex_part ID does not exist'])

        return cls(facsimile=facsimile_instance, success=True)


class UpdateFacsimile(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        bib_entry = ID(required=True)
        codex_part = ID(required=True)

    facsimile = Field(FacsimileNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('UpdateFacsimile.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))

        if Facsimile.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
            facsimile_instance = Facsimile.objects.get(pk=from_global_id(input.get('id'))[1])
        else:
            return cls(success=False, errors=['facsimile ID does not exist'])

        if BibEntry.objects.filter(pk=from_global_id(input.get('bib_entry'))[1]).exists():
            bib_entry = BibEntry.objects.get(pk=from_global_id(input.get('bib_entry'))[1])
            facsimile_instance.bib_entry = bib_entry
        else:
            return cls(success=False, errors=['bib_entry does not exist'])

        if CodexPart.objects.filter(pk=from_global_id(input.get('codex_part'))[1]).exists():
            codex_part = CodexPart.objects.get(pk=from_global_id(input.get('codex_part'))[1])
            facsimile_instance.codex_part = codex_part
        else:
            return cls(success=False, errors=['codex_part ID does not exist'])

        facsimile_instance.save()

        return cls(facsimile=facsimile_instance, success=True)


class DeleteFacsimile(relay.ClientIDMutation):
    class Input:
        id = ID()

    success = Boolean()
    errors = List(String)

    @classmethod
    @superuser_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('DeleteFacsimile.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))

        if input.get('id'):

            if Facsimile.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
                facsimile_instance = Facsimile.objects.get(pk=from_global_id(input.get('id'))[1])
                facsimile_instance.delete()
                return cls(success=True)

            else:
                return cls(success=False, errors=['facsimile ID does not exist'])

        else:
            return cls(success=False, errors=['facsimile ID is required'])


class Mutation(ObjectType):
    create_facsimile = CreateFacsimile.Field()
    update_facsimile = UpdateFacsimile.Field()
    #delete_facsimile = DeleteFacsimile.Field()
