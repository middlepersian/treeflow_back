from graphene import relay, InputObjectType, String, Field, ObjectType, List, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.dict.models import Dictionary


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


# Mutations

class CreateDictionary(relay.ClientIDMutation):
    class Input:
        name = String(required=True)
        slug = String(required=True)

    dictionary = Field(DictionaryNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, name, slug):
        # check that Dictionary does not exist same slug
        if Dictionary.objects.filter(slug=slug).exists():
            return cls(success=False)

        else:
            dictionary_instance = Dictionary.objects.create(name=name, slug=slug)
            dictionary_instance.save()
            return cls(dictionary=dictionary_instance, success=True)


class UpdateDictionary(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        name = String()
        slug = String()

    dictionary = Field(DictionaryNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, name, slug):

        if Dictionary.objects.filter(id=id).exists():

            dictionary_instance = Dictionary.objects.get(id=id)
            dictionary_instance.name = name
            dictionary_instance.slug = slug
            dictionary_instance.save()

            return cls(dictionary=dictionary_instance, success=True)
        else:
            return cls(success=False)


class DeleteDictionary(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):

        if Dictionary.objects.filter(id=id).exists():
            Dictionary.objects.get(id=id).delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_dictionary = CreateDictionary.Field()
    update_dictionary = UpdateDictionary.Field()
    delete_dictionary = DeleteDictionary.Field()
