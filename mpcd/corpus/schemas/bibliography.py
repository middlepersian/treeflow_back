import errno
from xmlrpc.client import Boolean
from graphene import relay, ObjectType, String, Field, ID, Boolean, List, Int
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
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

# Queries


class Query(ObjectType):
    bibentry = relay.Node.Field(BibEntryNode)
    all_bibentries = DjangoFilterConnectionField(BibEntryNode)


# Mutations


# Mutations
class CreateBibEntry(relay.ClientIDMutation):

    success = Boolean()

    class Input:
        title = String(required=True)
        year = Int(required=True)
        authors = List(AuthorInput)

    bibentry = Field(BibEntryNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, title, year, authors):
        logger.error('ROOT: {}'.format(root))
        # check that bybentry does not exist same title and year
        if BibEntry.objects.filter(title=title, year=year).exists():
            return cls(success=False)

        else:
            bibentry_instance = BibEntry.objects.create(title=title, year=year)

            for author in authors:
                if Author.objects.filter(name=author.name, last_name=author.last_name).exists():
                    author_instance = Author.objects.get(name=author.name, last_name=author.last_name)
                else:
                    author_instance = Author.objects.create(name=author.name, last_name=author.last_name)
                    author_instance.save()
                bibentry_instance.authors.add(author_instance)
            
            bibentry_instance.save()
            return cls(bibentry=bibentry_instance, success=True)


class Mutation(ObjectType):
    create_bibentry = CreateBibEntry.Field()
