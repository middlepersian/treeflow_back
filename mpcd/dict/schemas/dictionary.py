from graphene import relay, InputObjectType, String, Field, ObjectType, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required, superuser_required


from mpcd.dict.models import Dictionary
from mpcd.utils.normalize import to_nfc


class DictionaryNode(DjangoObjectType):
    class Meta:
        model = Dictionary
        filter_fields = {'name': ['exact', 'icontains', 'istartswith'],
                         'slug': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class DictionaryInput(InputObjectType):
    name = String()
    slug = String()

# Queries


class Query(ObjectType):
    dictionary = relay.Node.Field(DictionaryNode)
    all_dictionaries = DjangoFilterConnectionField(DictionaryNode)

    @login_required
    def resolve_all_dictionaries(self, info, **kwargs):
        return gql_optimizer.query(Dictionary.objects.all(), info)

# Mutations


class CreateDictionary(relay.ClientIDMutation):
    class Input:
        name = String(required=True)
        slug = String(required=True)

    dictionary = Field(DictionaryNode)
    success = Boolean()

    @classmethod
    @superuser_required

    def mutate_and_get_payload(cls, root, info, name, slug):
        name = to_nfc(name)
        slug = to_nfc(slug)
        dictionary_instance, dictionary_created = Dictionary.objects.get_or_create(name=name, slug=slug)
        return cls(dictionary=dictionary_instance, success=True)


class UpdateDictionary(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        name = String(required=True)
        slug = String(required=True)

    dictionary = Field(DictionaryNode)
    success = Boolean()

    @classmethod
    @login_required

    def mutate_and_get_payload(cls, root, info, id, name, slug):

        if Dictionary.objects.filter(pk=from_global_id(id)[1]).exists():

            dictionary_instance = Dictionary.objects.get(pk=from_global_id(id)[1])
            dictionary_instance.name = name
            dictionary_instance.slug = slug
            dictionary_instance.save()

            return cls(dictionary=dictionary_instance, success=True)
        else:
            return cls(dictionary=None, success=False)


class DeleteDictionary(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @classmethod
    @superuser_required

    def mutate_and_get_payload(cls, root, info, id):

        if Dictionary.objects.filter(pk=from_global_id(id)[1]).exists():
            Dictionary.objects.get(pk=from_global_id(id)[1]).delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_dictionary = CreateDictionary.Field()
    update_dictionary = UpdateDictionary.Field()
    delete_dictionary = DeleteDictionary.Field()
