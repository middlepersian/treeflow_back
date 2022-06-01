from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Codex, CodexPart


import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


from mpcd.utils.normalize import to_nfc

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class CodexPartNode(DjangoObjectType):
    class Meta:
        model = CodexPart
        filter_fields = {'codex__id': ['exact'],
                         'slug': ['exact', 'icontains', 'istartswith']}

        interfaces = (relay.Node, )


class CodexPartInput(InputObjectType):
    codex = ID(required=True)
    slug = String(required=True)

# Queries


class Query(ObjectType):

    codex_part = relay.Node.Field(CodexPartNode)
    all_codex_parts = DjangoFilterConnectionField(CodexPartNode)

    @login_required
    def resolve_all_codex_parts(self, info, **kwargs):
        return gql_optimizer.query(CodexPart.objects.all(), info)

# Mutations


class CreateCodexPart(relay.ClientIDMutation):
    class Input:
        codex = ID(required=True)
        slug = String(required=True)

    codex_part = Field(CodexPartNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('CreateCodexPart.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))

        if Codex.objects.filter(pk=from_global_id(input.get('codex'))[1]).exists():
            codex = Codex.objects.get(pk=from_global_id(input.get('codex'))[1])
            codex_part_instance, codex_part_created = CodexPart.objects.get_or_create(codex=codex)
            codex_part_instance.slug = to_nfc(input.get('slug'))
            codex_part_instance.save()
        else:
            return cls(success=False, errors=['Codex ID does not exist'])

        return cls(codex_part=codex_part_instance, success=True, errors=[])


class UpdateCodexPart(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        codex = ID(required=True)
        slug = String(required=True)

    codex_part = Field(CodexPartNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('UpdateCodexPart.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))

        if CodexPart.objects.filter(pk=from_global_id(input.get('codex_part'))[1]).exists():
            codex_part = CodexPart.objects.get(pk=from_global_id(input.get('codex_part'))[1])
        else:
            return cls(success=False, errors=['Codex_Part ID does not exist'])

        # update codex
        if Codex.objects.filter(pk=from_global_id(input.get('codex'))[1]).exists():
            codex = Codex.objects.get(pk=from_global_id(input.get('codex'))[1])
            codex_part.codex = codex
        else:
            return cls(success=False, errors=['Codex ID does not exist'])

       # update slug
        codex_part.slug = to_nfc(input.get('slug'))

        codex_part.save()
        return cls(codex_part=codex_part, success=True)


class DeleteCodexPart(relay.ClientIDMutation):
    class Input:
        codex_part = ID(required=True)

    codex_part = Field(CodexPartNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('DeleteCodexPart.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))

        if CodexPart.objects.filter(pk=from_global_id(input.get('codex_part'))[1]).exists():
            codex_part = CodexPart.objects.get(pk=from_global_id(input.get('codex_part'))[1])
        else:
            return cls(success=False, errors=['codex_part does not exist'])

        codex_part.delete()
        return cls(codex_part=codex_part, success=True)


class Mutation(ObjectType):
    create_codex_part = CreateCodexPart.Field()
    update_codex_part = UpdateCodexPart.Field()
    delete_codex_part = DeleteCodexPart.Field()
