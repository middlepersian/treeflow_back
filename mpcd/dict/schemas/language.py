
from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.dict.models import Language


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class LanguageNode(DjangoObjectType):
    class Meta:
        model = Language
        filter_fields = {'identifier': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class LanguageInput(InputObjectType):
    identifier = String()


# Queries

class Query(ObjectType):
    language = relay.Node.Field(LanguageNode)
    all_languages = DjangoFilterConnectionField(LanguageNode)

# Mutations


class CreateLanguage(relay.ClientIDMutation):
    class Input:
        identifier = String(required=True)

    language = Field(LanguageNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, identifier):
        # check that bybentry does not exist same title and year
        if Language.objects.filter(identifier=identifier).exists():
            return cls(success=False)

        else:
            language_instance = Language.objects.create(identifier=identifier)
            return cls(language=language_instance, success=True)


class UpdateLanguage(relay.ClientIDMutation):
    class Input:
        identifier = String(required=True)

    language = Field(LanguageNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, identifier):

        if Language.objects.filter(identifier=identifier).exists():
            language_instance = Language.objects.get(identifier=identifier)
            language_instance.identifier = identifier
            language_instance.save()

            return cls(language=language_instance, success=True)

        else:
            return cls(success=False)


class DeleteLanguage(relay.ClientIDMutation):
    class Input:
        id = ID()

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        if Language.objects.filter(id=id).exists():
            language_instance = Language.objects.get(id=id)
            language_instance.delete()
            return cls(success=True)

        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_language = CreateLanguage.Field()
    update_language = UpdateLanguage.Field()
    delete_language = DeleteLanguage.Field()
