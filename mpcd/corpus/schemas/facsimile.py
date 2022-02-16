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
        interfaces = (relay.Node, )


class FacsimileInput(InputObjectType):
    reference = ID()
    codex_part = ID()

# Queries


class Query(ObjectType):
    facsimile = relay.Node.Field(FacsimileNode)
    all_facsimiles = DjangoFilterConnectionField(FacsimileNode)


# Mutations

class CreateFacsimile(relay.ClientIDMutation):
    class Input:
        reference = ID()
        codex_part = ID()

    facsimile = Field(FacsimileNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('CreateFacsimile.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))

        if input.get('reference', None) is not None:

            if BibEntry.objects.filter(pk=from_global_id(input.get('reference'))[1]).exists():
                reference = BibEntry.objects.get(pk=from_global_id(input.get('reference'))[1])
                facsimile_instance = Facsimile.objects.create(reference=reference)
            else:
                return cls(success=False, errors=['reference does not exist'])

        else:
            return cls(success=False, errors=['reference is required'])

        if input.get('codex_part', None) is not None:

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
        reference = ID()
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

        if input.get('reference', None) is not None:

            if BibEntry.objects.filter(pk=from_global_id(input.get('reference'))[1]).exists():
                reference = BibEntry.objects.get(pk=from_global_id(input.get('reference'))[1])
                facsimile_instance.reference = reference
            else:
                return cls(success=False, errors=['reference does not exist'])

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
        facsimile = ID()

    facsimile = Field(FacsimileNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('DeleteFacsimile.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))

        if input.get('facsimile', None) is not None:

            if Facsimile.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
                facsimile_instance = Facsimile.objects.get(pk=input.get('id')[1])
            else:
                return cls(success=False, errors=['facsimile does not exist'])

        else:
            return cls(success=False, errors=['facsimile ID is required'])

        facsimile_instance.delete()
        return cls(facsimile=facsimile_instance, success=True)


class Mutation(ObjectType):
    create_facsimile = CreateFacsimile.Field()
    update_facsimile = UpdateFacsimile.Field()
    delete_facsimile = DeleteFacsimile.Field()
