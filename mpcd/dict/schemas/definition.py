from graphene import relay, InputObjectType, String, Field, ObjectType, ID, Boolean, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer

from mpcd.dict.models import Definition


class DefinitionNode(DjangoObjectType):
    class Meta:
        model = Definition
        filter_fields = {'definition': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class DefinitionInput(InputObjectType):
    definition = String()
    language = String()

# Queries


class Query(ObjectType):
    definition = relay.Node.Field(DefinitionNode)
    all_definitions = DjangoFilterConnectionField(DefinitionNode)

    def resolve_all_definitions(self, info, **kwargs):
        return gql_optimizer.query(Definition.objects.all(), info)


# Mutations


class CreateDefinition(relay.ClientIDMutation):
    class Input:
        definition = String()
        language = String()

    definition = Field(DefinitionNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        if input.get('definition', None) is not None:
            definition_input = input.get('definition')
            if input.get('language', None) is not None:
                language_input = input.get('language')

                definition_instance, definition_created = Definition.objects.get_or_create(
                    definition=definition_input, language=language_input)
                definition_instance.save()
                return cls(definition=definition_instance, success=True)

            else:
                return cls(definition=None, success=False, errors=['language is required'])

        else:
            return cls(definition=None, success=False, errors=['No definition input'])


class UpdateDefinition(relay.ClientIDMutation):
    class Input:
        id = ID()
        definition = DefinitionInput()
        language = String()

    definition = Field(DefinitionNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # check that Definition  does not exist

        if input.get('id', None) is not None:

            if Definition.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
                if input.get('definition', None) is not None:
                    definition_input = input.get('definition')
                    if input.get('language', None) is not None:
                        language_input = input.get('language')
                        definition_instance, definition_created = Definition.objects.get_or_create(
                            definition=definition_input, language=language_input)
                        definition_instance.save()
                        return cls(definition=definition_instance, success=True)
                    else:
                        return cls(definition=None, success=False, errors=['language is required'])
                else:
                    return cls(definition=None, success=False, errors=['No definition input'])


class DeleteDefinition(relay.ClientIDMutation):
    class Input:
        id = ID()

    success = Boolean()

    @ classmethod
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
