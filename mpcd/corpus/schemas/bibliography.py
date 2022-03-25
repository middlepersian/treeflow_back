from graphene import relay, ObjectType, String, Field, ID, Boolean, List, Int, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Author, BibEntry
from mpcd.corpus.schemas.author import AuthorInput

import graphene_django_optimizer as gql_optimizer
from mpcd.utils.normalize import to_nfc


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class BibEntryNode(DjangoObjectType):
    class Meta:
        model = BibEntry
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'year': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)


class BibEntryInput(InputObjectType):
    title = String()
    year = Int()
    authors = List(AuthorInput)


# Queries

class Query(ObjectType):
    bibentry = relay.Node.Field(BibEntryNode)
    all_bibentries = DjangoFilterConnectionField(BibEntryNode)

    def resolve_all_bibentries(self, info, **kwargs):
        return gql_optimizer.query(BibEntry.objects.all(), info)

# Mutations


class CreateBibEntry(relay.ClientIDMutation):
    class Input:
        title = String(required=True)
        year = Int(required=True)
        authors = List(AuthorInput)

    bibentry = Field(BibEntryNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.error("input: {}".format(input))
        bibentry_instance, bibentry_created = BibEntry.objects.get_or_create(
            title=to_nfc(input.get('title')), year=to_nfc(input.get('year')))

        authors = input.get('authors', None)
        for author in authors:
            author_instance, author_created = Author.objects.get_or_create(
                name=to_nfc(author.get('name', None)),
                last_name=to_nfc(author.get('last_name', None)))
            bibentry_instance.authors.add(author_instance)
        bibentry_instance.save()
        return cls(bibentry=bibentry_instance, success=True)


class UpdateBibEntry(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        title = String(required=True)
        year = Int(required=True)
        authors = List(AuthorInput)

    bibentry = Field(BibEntryNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        if BibEntry.objects.filter(pk=from_global_id(id)[1]).exists():
            bibentry_instance = BibEntry.objects.get(pk=from_global_id(id)[1])
        else:
            return cls(success=False, errors=['BibEntry does not exist'])

        bibentry_instance.title = to_nfc(input.get('title'))
        bibentry_instance.year = to_nfc(input.get('year'))

        if input.get('authors', None) is not None:
            bibentry_instance.authors.clear()
            authors = input.get('authors', None)
            for author in authors:
                author_instance, author_created = Author.objects.get_or_create(
                    first_name=to_nfc(author.get('first_name', None)),
                    last_name=to_nfc(author.get('last_name', None)))
                bibentry_instance.authors.add(author_instance)

        bibentry_instance.save()
        return cls(bibentry=bibentry_instance, success=True)


class DeleteBibEntry(relay.ClientIDMutation):

    success = Boolean()

    class Input:
        id = ID(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        if BibEntry.objects.filter(pk=from_global_id(id[1])).exists():
            bibentry_instance = BibEntry.objects.get(pk=from_global_id(id)[1])
            bibentry_instance.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_bibentry = CreateBibEntry.Field()
    delete_bibentry = DeleteBibEntry.Field()
    update_bibentry = UpdateBibEntry.Field()
