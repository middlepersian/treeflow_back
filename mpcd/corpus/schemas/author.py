from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer

from mpcd.corpus.models import Author
from mpcd.utils.normalize import to_nfc


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class AuthorNode(DjangoObjectType):
    class Meta:
        model = Author
        filter_fields = {'name': ['exact', 'icontains', 'istartswith'],
                         'last_name': ['exact', 'icontains', 'istartswith']
                         }
        interfaces = (relay.Node,)


class AuthorInput(InputObjectType):
    name = String(required=True)
    last_name = String(required=True)

# Queries


class Query(ObjectType):
    author = relay.Node.Field(AuthorNode)
    all_authors = DjangoFilterConnectionField(AuthorNode)

    def resolve_all_authors(self, info, **kwargs):
        return gql_optimizer.query(Author.objects.all(), info)


# Mutations
class CreateAuthor(relay.ClientIDMutation):

    class Input:
        name = String(required=True)
        last_name = String(required=True)

    author = Field(AuthorNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.error('author_inpuut: {}'.format(input))

        # check if author exists, if not create it
        author_instance, author_created = Author.objects.get_or_create(
            name=to_nfc(input.get('name')), last_name=to_nfc(input.get('last_name')))

        return cls(author=author_instance, success=True, errors=None)


class UpdateAuthor(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        name = String(required=True)
        last_name = String(required=True)

    author = Field(AuthorNode)

    @ classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if Author.objects.filter(pk=from_global_id(id)[1]).exists():
            author_instance = Author.objects.get(pk=from_global_id(id)[1])
            author_instance.name = to_nfc(input.get('name'))
            author_instance.last_name = to_nfc(input.get('last_name'))
            author_instance.save()
            return cls(author=author_instance, success=True)
        else:
            return cls(errors=['Author ID does not exist'], success=False)


class DeleteAuthor(relay.ClientIDMutation):

    class Input:
        id = ID(required=True)

    # return values
    author = Field(AuthorNode)
    id = ID()
    message = String()

    @ classmethod
    def mutate_and_get_payload(cls, root, info, id):
        author = Author.objects.get(pk=from_global_id(id)[1])
        author.delete()
        return cls(id=id, message='Author deleted')


class Mutation(ObjectType):
    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()
    delete_author = DeleteAuthor.Field()
