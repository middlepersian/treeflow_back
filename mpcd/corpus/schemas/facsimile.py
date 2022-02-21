from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import BibEntry, Facsimile, CodexPart


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
    bib_entry = ID()
    codex_part = ID()

# Queries


class Query(ObjectType):
    facsimile = relay.Node.Field(FacsimileNode)
    all_facsimiles = DjangoFilterConnectionField(FacsimileNode)


# Mutations

class CreateFacsimile(relay.ClientIDMutation):
    class Input:
        bib_entry = ID()
        codex_part = ID()

    facsimile = Field(FacsimileNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('CreateFacsimile.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))

        if input.get('bib_entry', None) is not None:

            if BibEntry.objects.filter(pk=from_global_id(input.get('bib_entry'))[1]).exists():
                bib_entry = BibEntry.objects.get(pk=from_global_id(input.get('bib_entry'))[1])
                facsimile_instance = Facsimile.objects.create(bib_entry=bib_entry)
            else:
                return cls(success=False, errors=['bib_entry does not exist'])

        else:
            return cls(success=False, errors=['bib_entry is required'])

        if input.get('codex_part', None) is not None and input.get('codex_part', None) != "":

            if CodexPart.objects.filter(pk=from_global_id(input.get('codex_part'))[1]).exists():
                codex_part = CodexPart.objects.get(pk=from_global_id(input.get('codex_part'))[1])
                facsimile_instance.codex_part = codex_part
            else:
                return cls(success=False, errors=['codex_part does not exist'])

        facsimile_instance.save()

        return cls(facsimile=facsimile_instance, success=True)


class UpdateFacsimile(relay.ClientIDMutation):
    class Input:
        facsimile = ID()
        bib_entry = ID()
        codex_part = ID()

    facsimile = Field(FacsimileNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('UpdateFacsimile.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))

        if input.get('facsimile', None) is not None:

            if Facsimile.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
                facsimile_instance = Facsimile.objects.get(pk=from_global_id(input.get('id'))[1])
            else:
                return cls(success=False, errors=['facsimile does not exist'])

        else:
            return cls(success=False, errors=['facsimile ID is required'])

        if input.get('bib_entry', None) is not None:

            if BibEntry.objects.filter(pk=from_global_id(input.get('bib_entry'))[1]).exists():
                bib_entry = BibEntry.objects.get(pk=from_global_id(input.get('bib_entry'))[1])
                facsimile_instance.bib_entry = bib_entry
            else:
                return cls(success=False, errors=['bib_entry does not exist'])

        if input.get('codex_part', None) is not None:

            if CodexPart.objects.filter(pk=from_global_id(input.get('codex_part'))[1]).exists():
                codex_part = CodexPart.objects.get(pk=from_global_id(input.get('codex_part'))[1])
                facsimile_instance.codex_part = codex_part
            else:
                return cls(success=False, errors=['codex_part does not exist'])

        facsimile_instance.save()

        return cls(facsimile=facsimile_instance, success=True)


class DeleteFacsimile(relay.ClientIDMutation):
    class Input:
        id = ID()

    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('DeleteFacsimile.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))

        if input.get('id', None) is not None:

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
    delete_facsimile = DeleteFacsimile.Field()
