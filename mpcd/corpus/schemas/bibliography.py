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
        filter_fields = {'authors': ['exact', 'icontains', 'istartswith'],
                         'title': ['exact', 'icontains', 'istartswith'],
                         'year': ['exact', 'icontains', 'istartswith'],
                         }
        interfaces = (relay.Node,)


class BibEntryInput(InputObjectType):
    title = String()
    year = String()
    authors = List(AuthorInput)


# Queries

class Query(ObjectType):
    bibentry = relay.Node.Field(BibEntryNode)
    all_bibentries = DjangoFilterConnectionField(BibEntryNode)


# Mutations
class CreateBibEntry(relay.ClientIDMutation):
    class Input:
        title = String(required=True)
        year = Int(required=True)
        authors = List(AuthorInput)

    bibentry = Field(BibEntryNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, title, year, authors):
        # check that bybentry does not exist same title and year
        if BibEntry.objects.filter(title=title, year=year).exists():
            return cls(success=False)

        else:
            bibentry_instance = BibEntry.objects.create(title=title, year=year)

            for author in authors:
                # check if author exists
                if Author.objects.filter(name=author.name, last_name=author.last_name).exists():
                    author_instance = Author.objects.get(name=author.name, last_name=author.last_name)
                else:
                    # create it
                    author_instance = Author.objects.create(name=author.name, last_name=author.last_name)
                    author_instance.save()
                bibentry_instance.authors.add(author_instance)

            bibentry_instance.save()
            return cls(bibentry=bibentry_instance, success=True)


class UpdateBibEntry(relay.ClientIDMutation):
    class Input:
        id = ID()
        title = String(required=True)
        year = Int(required=True)
        authors = List(AuthorInput)

    bibentry = Field(BibEntryNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, title, year, authors, id):
        # check that bib exists with id
        if BibEntry.objects.filter(id=id).exists():
            bibentry_instance = BibEntry.objects.get(pk=from_global_id(id)[1])
            bibentry_instance.title = title
            bibentry_instance.year = year
            bibentry_instance.save()

            # delete all authors
            bibentry_instance.authors.clear()

            for author in authors:
                # check if author exists
                if Author.objects.filter(name=author.name, last_name=author.last_name).exists():
                    author_instance = Author.objects.get(name=author.name, last_name=author.last_name)
                else:
                    # create it
                    author_instance = Author.objects.create(name=author.name, last_name=author.last_name)
                    author_instance.save()
                bibentry_instance.authors.add(author_instance)

            bibentry_instance.save()
            return cls(bibentry=bibentry_instance, success=True)
        else:
            return cls(success=False)


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
