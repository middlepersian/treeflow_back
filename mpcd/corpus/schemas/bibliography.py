from graphene import relay, ObjectType, String, Field, ID, Boolean, List, Int, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Author, BibEntry
from mpcd.corpus.schemas.author import AuthorInput


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


# Mutations
class CreateBibEntry(relay.ClientIDMutation):
    class Input:
        title = String()
        year = Int()
        authors = List(AuthorInput)

    bibentry = Field(BibEntryNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # check that bybentry does not exist same title and year
        logger.error("input: {}".format(input))

        if input.get('title', None) is not None:
            title = input.get('title')
            bibentry_instance = BibEntry.objects.create(title=title)
        else:
            return cls(success=False, errors=['title is required'])

        if input.get('year', None) is not None:
            year = input.get('year')
            logger.error("year: {}".format(year))
            bibentry_instance.year = year

        if input.get('authors', None) is not None:
            authors = input.get('authors', None)
            for author in authors:
                author_instance, author_created = Author.objects.get_or_create(
                    name=author.get('name', None),
                    last_name=author.get('last_name', None))
                bibentry_instance.authors.add(author_instance)
        bibentry_instance.save()
        return cls(bibentry=bibentry_instance, success=True)


class UpdateBibEntry(relay.ClientIDMutation):
    class Input:
        id = ID()
        title = String()
        year = Int()
        authors = List(AuthorInput)

    bibentry = Field(BibEntryNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        if input.get('id', None) is not None:
            if BibEntry.objects.filter(pk=from_global_id(id)[1]).exists():
                bibentry_instance = BibEntry.objects.get(pk=from_global_id(id)[1])
            else:
                return cls(success=False, errors=['bibentry does not exist'])

            if input.get('title', None) is not None:
                title = input.get('title', None)
                bibentry_instance.title = title

            if input.get('authors', None) is not None:
                bibentry_instance.authors.clear()
                authors = input.get('authors', None)
                for author in authors:
                    author_instance, author_created = Author.objects.get_or_create(
                        first_name=author.get('first_name', None),
                        last_name=author.get('last_name', None))
                    bibentry_instance.authors.add(author_instance)

            bibentry_instance.save()
            return cls(bibentry=bibentry_instance, success=True)

        else:
            return cls(success=False, errors=['id is required'])


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
