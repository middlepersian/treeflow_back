from calendar import c
from graphene import relay, ObjectType, String, Field, ID, Boolean, List, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.corpus.models import Codex, Author
from .author import AuthorInput
from .bibliography import BibEntry, BibEntryInput
from graphql_relay import from_global_id


import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required, superuser_required


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class CodexNode(DjangoObjectType):
    class Meta:
        model = Codex
        filter_fields = {'sigle': ['exact', 'icontains', 'istartswith'],
                         'title': ['exact', 'icontains', 'istartswith'],

                         'copy_date': ['exact', 'icontains', 'istartswith'],
                         'copy_place_name': ['exact', 'icontains', 'istartswith'],
                         'copy_place_latitude': ['exact', 'icontains', 'istartswith'],
                         'copy_place_longitude': ['exact', 'icontains', 'istartswith'],

                         'library': ['exact', 'icontains', 'istartswith'],
                         'signature': ['exact', 'icontains', 'istartswith']
                         }
        interfaces = (relay.Node,)


class CodexInput(InputObjectType):
    sigle = String()
    title = String()
    copy_date = String()
    copy_place_name = String()
    copy_place_latitude = String()
    copy_place_longitude = String()
    library = String()
    signature = String()
    scribes = List(AuthorInput)
    facsimiles = List(BibEntryInput)


class Query(ObjectType):
    codex = relay.Node.Field(CodexNode)
    all_codex = DjangoFilterConnectionField(CodexNode)

    @login_required
    def resolve_all_codex(self, info, **kwargs):
        return gql_optimizer.query(Codex.objects.all(), info)

# Mutations


class CreateCodex(relay.ClientIDMutation):
    class Input:
        sigle = String(required=True)
        title = String(required=True)

        copy_date = String(required=False)
        copy_place_name = String(required=False)
        copy_place_latitude = String(required=False)
        copy_place_longitude = String(required=False)

        library = String(required=False)
        signature = String(required=False)
        scribes = List(AuthorInput)
        facsimiles = List(BibEntryInput)

    codex = Field(CodexNode)
    success = Boolean()
    errors = List(String)

    @login_required
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # check sigle is provided and that codex does not already exist with same sigle
        if input.get('sigle', None) is None:
            return cls(success=False, errors=["No sigle provided"])

        else:
            if Codex.objects.filter(sigle=input.get('sigle')).exists():
                return cls(success=False, errors=[{'message': 'Codex with the same sigle already exists'}])

        # check that title is provided
        if input.get('title', None) is None:
            return cls(success=False, errors=["No title provided"])

        else:

            codex_instance = Codex.objects.create(sigle=input.get('sigle'), title=input.get('title'))

            if input.get('copy_date', None) is not None:
                codex_instance.copy_date = input.get('copy_date')
            if input.get('copy_place_name', None) is not None:
                codex_instance.copy_place_name = input.get('copy_place_name')
            if input.get('copy_place_latitude', None) is not None:
                codex_instance.copy_place_latitude = input.get('copy_place_latitude')
            if input.get('copy_place_longitude', None) is not None:
                codex_instance.copy_place_longitude = input.get('copy_place_longitude')
            if input.get('library', None) is not None:
                codex_instance.library = input.get('library')
            if input.get('signature', None) is not None:
                codex_instance.signature = input.get('signature')

            if input.get('scribes', None) is not None:
                for scribe in input.get('scribes'):
                    author_instance, author_created = Author.objects.get_or_create(
                        name=scribe.name, last_name=scribe.last_name)
                    author_instance.save()
                codex_instance.authors.add(author_instance)
           # TODO implement facsimiles
            codex_instance.save()
            return cls(codex=codex_instance, success=True)


class UpdateCodex(relay.ClientIDMutation):
    class Input:
        sigle = String(required=True)
        title = String(required=True)

        copy_date = String(required=False)
        copy_place_name = String(required=False)
        copy_place_latitude = String(required=False)
        copy_place_longitude = String(required=False)

        library = String(required=False)
        signature = String(required=False)
        scribes = List(AuthorInput)
        facsimiles = List(BibEntryInput)

    codex = Field(CodexNode)
    success = Boolean()

    @login_required
    @classmethod
    def mutate_and_get_payload(cls, root, info, sigle, title, copy_date, copy_place_name, copy_place_latitude, copy_place_longitude, library, signature, scribes, facsimiles):
        # check that bib exists with id
        if Codex.objects.filter(pk=from_global_id(id)[1]).exists():
            codex_instance = Codex.objects.get(id=id)
            codex_instance.sigle = sigle
            codex_instance.title = title
            codex_instance.copy_date = copy_date
            codex_instance.copy_place_name = copy_place_name
            codex_instance.copy_place_latitude = copy_place_latitude
            codex_instance.copy_place_longitude = copy_place_longitude
            codex_instance.library = library
            codex_instance.signature = signature

            # clear authors
            codex_instance.authors.clear()
            for author in scribes:
                # check if author exists
                if Author.objects.filter(name=author.name, last_name=author.last_name).exists():
                    author_instance = Author.objects.get(name=author.name, last_name=author.last_name)
                else:
                    # create it
                    author_instance = Author.objects.create(name=author.name, last_name=author.last_name)
                    author_instance.save()

                codex_instance.authors.add(author_instance)

            # clear facsimiles
            codex_instance.facsimiles.clear()
            for facsimile in facsimiles:
                # check if bibentry exists
                if BibEntry.objects.filter(pk=from_global_id(facsimile.id)[1]).exists():

                    bibentry_instance = BibEntry.objects.get(pk=from_global_id(facsimile.id)[1])
                else:
                    # create it
                    bibentry_instance = BibEntry.objects.create(title=facsimile.title, year=facsimile.year)
                    for bib_author in facsimile.authors:
                        # check if author exists
                        if Author.objects.filter(name=bib_author.name, last_name=bib_author.last_name).exists():
                            author_instance = Author.objects.get(name=bib_author.name, last_name=bib_author.last_name)
                        else:
                            # create it
                            author_instance = Author.objects.create(
                                name=bib_author.name, last_name=bib_author.last_name)
                            author_instance.save()
                        bibentry_instance.authors.add(author_instance)

                    bibentry_instance.save()

                codex_instance.facsimiles.add(bibentry_instance)
            codex_instance.save()
            return cls(codex=codex_instance, success=True)
        else:
            return cls(success=False)


class DeleteCodex(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @superuser_required
    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        # check that codex exists with id
        if Codex.objects.filter(pk=from_global_id(id)[1]).exists():
            codex_instance = Codex.objects.get(pk=from_global_id(id)[1])
            codex_instance.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_codex = CreateCodex.Field()
    delete_codex = DeleteCodex.Field()
    update_codex = UpdateCodex.Field()
