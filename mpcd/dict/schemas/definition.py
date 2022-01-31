from graphene import relay, InputObjectType, String, Field, ObjectType, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.dict.models import Definition, Language
from graphql_relay import from_global_id
from mpcd.dict.schemas import LanguageInput


class DefinitionNode(DjangoObjectType):
    class Meta:
        model = Definition
        filter_fields = {'definition': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class DefinitionInput(InputObjectType):
    definition = String()
    language = LanguageInput()

# Queries


class Query(ObjectType):
    definition = relay.Node.Field(DefinitionNode)
    all_definitions = DjangoFilterConnectionField(DefinitionNode)

# Mutations


class CreateDefinition(relay.ClientIDMutation):
    class Input:
        definition = DefinitionInput()
        language = LanguageInput()

    definition = Field(DefinitionNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, definition, id, language):
        # check that Definition  does not exist
        if Definition.objects.filter(pk=from_global_id(id)[1]).exists():
            return cls(success=False)

        else:
            definition_instance = Definition.objects.create(definition=definition)
            if Language.objects.filter(pk=from_global_id(language.id)[1]).exists():
                language_instance = Language.objects.get(pk=from_global_id(id)[1])
                definition_instance.language = language_instance
            definition_instance.save()
            return cls(definition=definition_instance, success=True)


class UpdateDefinition(relay.ClientIDMutation):
    class Input:
        id = ID()
        definition = DefinitionInput()
        language = LanguageInput()

    definition = Field(DefinitionNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, definition, language):
        # check that Definition  does not exist
        if Definition.objects.filter(id=id).exists():
            definition_instance = Definition.objects.get(pk=from_global_id(id)[1])
            if Language.objects.filter(pk=from_global_id(language.id)[1]).exists():
                language_instance = Language.objects.get(pk=from_global_id(language.id)[1])
                definition_instance.language = language_instance
            definition_instance.definition = definition
            definition_instance.save()
            return cls(definition=definition_instance, success=True)
        else:
            return cls(success=False)


class DeleteDefinition(relay.ClientIDMutation):
    class Input:
        id = ID()

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        # check that Definition  does not exist
        if Definition.objects.filter(id=id).exists():
            definition_instance = Definition.objects.get(pk=from_global_id(id)[1])
            definition_instance.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_definition = CreateDefinition.Field()
    update_definition = UpdateDefinition.Field()
    delete_definition = DeleteDefinition.Field()
