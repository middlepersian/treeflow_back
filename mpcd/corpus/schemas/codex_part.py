from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Codex, CodexPart


import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class CodexPartNode(DjangoObjectType):
    class Meta:
        model = CodexPart
        filter_fields = {'part_type': ['exact', 'icontains', 'istartswith'],
                         'part_number': ['exact', 'icontains', 'istartswith'],
                         'description': ['exact', 'icontains', 'istartswith']}

        interfaces = (relay.Node, )


class CodexPartInput(InputObjectType):
    codex = ID()
    part_type = String()
    part_number = String()
    description = String()

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
        codex = ID()
        part_type = String()
        part_number = String()
        description = String()

    codex_part = Field(CodexPartNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required

    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('CreateCodexPart.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))

        if input.get('codex', None) is not None:

            if Codex.objects.filter(pk=from_global_id(input.get('codex'))[1]).exists():
                codex = Codex.objects.get(pk=from_global_id(input.get('codex'))[1])
                codex_part_instance = CodexPart.objects.create(codex=codex)
            else:
                return cls(success=False, errors=['codex does not exist'])

        else:
            return cls(success=False, errors=['codex ID is required'])

        if input.get('part_type', None) is not None:
            codex_part_instance.part_type = input.get('part_type')

        if input.get('part_number', None) is not None:
            codex_part_instance.part_number = input.get('part_number')

        if input.get('description', None) is not None:
            codex_part_instance.description = input.get('description')

        codex_part_instance.save()

        return cls(codex_part=codex_part_instance, success=True, errors=[])


class UpdateCodexPart(relay.ClientIDMutation):
    class Input:
        codex_part = ID()
        codex = ID()
        part_type = String()
        part_number = String()
        description = String()

    codex_part = Field(CodexPartNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required

    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('UpdateCodexPart.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))

        if input.get('codex_part', None) is not None:

            if CodexPart.objects.filter(pk=from_global_id(input.get('codex_part'))[1]).exists():
                codex_part = CodexPart.objects.get(pk=from_global_id(input.get('codex_part'))[1])
            else:
                return cls(success=False, errors=['codex_part does not exist'])

        else:
            return cls(success=False, errors=['codex_part ID is required'])

        if input.get('codex', None) is not None:

            if Codex.objects.filter(pk=from_global_id(input.get('codex'))[1]).exists():
                codex = Codex.objects.get(pk=from_global_id(input.get('codex'))[1])
                codex_part.codex = codex
            else:
                return cls(success=False, errors=['codex does not exist'])

        if input.get('part_type', None) is not None:
            codex_part.part_type = input.get('part_type')

        if input.get('part_number', None) is not None:
            codex_part.part_number = input.get('part_number')

        if input.get('description', None) is not None:
            codex_part.description = input.get('description')

        codex_part.save()
        return cls(codex_part=codex_part, success=True)


class DeleteCodexPart(relay.ClientIDMutation):
    class Input:
        codex_part = ID()

    codex_part = Field(CodexPartNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.debug('DeleteCodexPart.mutate_and_get_payload()')
        logger.debug('input: {}'.format(input))

        if input.get('codex_part', None) is not None:

            if CodexPart.objects.filter(pk=from_global_id(input.get('codex_part'))[1]).exists():
                codex_part = CodexPart.objects.get(pk=from_global_id(input.get('codex_part'))[1])
            else:
                return cls(success=False, errors=['codex_part does not exist'])

        else:
            return cls(success=False, errors=['codex_part ID is required'])

        codex_part.delete()
        return cls(codex_part=codex_part, success=True)


class Mutation(ObjectType):
    create_codex_part = CreateCodexPart.Field()
    update_codex_part = UpdateCodexPart.Field()
    delete_codex_part = DeleteCodexPart.Field()
