from graphene import relay, ObjectType, String, Field, ID
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Author


class AuthorNode(DjangoObjectType):
    class Meta:
        model = Author
        filter_fields = {'name': ['exact', 'icontains', 'istartswith'],
                         'last_name': ['exact', 'icontains', 'istartswith']
                         }
        interfaces = (relay.Node,)


class Query(ObjectType):
    author = relay.Node.Field(AuthorNode)
    all_authors = DjangoFilterConnectionField(AuthorNode)


# Mutations


class CreateAuthor(relay.ClientIDMutation):
    class Input:
        name = String(required=True)
        last_name = String(required=True)

    author = Field(AuthorNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, name, last_name):
        # check that author does not exist same name and last name
        author = Author.objects.filter(name=name, last_name=last_name)
        if not author:
            author_instance = Author(name=name, last_name=last_name)
            author_instance.save()
            return CreateAuthor(author=author_instance)


class UpdateAuthor(relay.ClientIDMutation):
    class Input:
        id = ID()
        name = String(required=True)
        last_name = String(required=True)

    author = Field(AuthorNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, name, last_name, id):
        author = Author.objects.get(pk=from_global_id(id)[1])
        author.name = name
        author.last_name = last_name
        author.save()
        return UpdateAuthor(author=author)


class DeleteAuthor(relay.ClientIDMutation):
    # return values
    id = ID()
    message = String()

    class Input:
        id = ID()

    author = Field(AuthorNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        author = Author.objects.get(pk=from_global_id(id)[1])
        author.delete()
        return DeleteAuthor(id=id, message='Author deleted')


class Mutation(ObjectType):
    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()
    delete_author = DeleteAuthor.Field()
