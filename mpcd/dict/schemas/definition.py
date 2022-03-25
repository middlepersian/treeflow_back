from numpy import require
from graphene import relay, InputObjectType, String, Field, ObjectType, ID, Boolean, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer

from mpcd.dict.models import Definition
from mpcd.utils.normalize import to_nfc


class DefinitionNode(DjangoObjectType):
    class Meta:
        model = Definition
        filter_fields = {'definition': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class DefinitionInput(InputObjectType):
    definition = String(required=True)
    language = String(required=True)

# Queries


class Query(ObjectType):
    definition = relay.Node.Field(DefinitionNode)
    all_definitions = DjangoFilterConnectionField(DefinitionNode)

    def resolve_all_definitions(self, info, **kwargs):
        return gql_optimizer.query(Definition.objects.all(), info)


# Mutations


class CreateDefinition(relay.ClientIDMutation):
    class Input:
        definition = String(required=True)
        language = String(required=True)

    definition = Field(DefinitionNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        # normalize input
        definition_input = to_nfc(input.get('definition'))
        language_input = to_nfc(input.get('language'))
        definition_instance, definition_created = Definition.objects.get_or_create(
            definition=definition_input, language=language_input)
        return cls(definition=definition_instance, success=True)


class UpdateDefinition(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        definition = DefinitionInput(required=True)
        language = String(required=True)

    definition = Field(DefinitionNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # check that Definition  does not exist

        if Definition.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
            definition_instance = Definition.objects.get(pk=from_global_id(input.get('id'))[1])
            # normalize input
            definition_input = to_nfc(input.get('definition'))
            language_input = to_nfc(input.get('language'))
            definition_instance.definition = definition_input
            definition_instance.language = language_input
            definition_instance.save()
            return cls(definition=definition_instance, success=True)
        else:
            return cls(errors=['Definition ID does not exist'], success=False)


class DeleteDefinition(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        # check that Definition  does not exist
        if Definition.objects.filter(pk=from_global_id('id')[1]).exists():
            definition_instance = Definition.objects.get(pk=from_global_id(id)[1])
            definition_instance.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_definition = CreateDefinition.Field()
    update_definition = UpdateDefinition.Field()
    delete_definition = DeleteDefinition.Field()
