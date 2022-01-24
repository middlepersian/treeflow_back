from app_backend.mpcd.corpus.models.bibliography import BibEntry
from graphene import relay, ObjectType, String, Field, ID, Boolean, List, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.corpus.models import Codex, Author
from mpcd.corpus.schemas.author import AuthorInput
from mpcd.corpus.schemas.bibliography import BibEntryInput

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
                         'signature': ['exact', 'icontains', 'istartswith'],
                         'scribes': ['exact', 'icontains', 'istartswith'],
                         'facsimiles': ['exact', 'icontains', 'istartswith'],

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

    @classmethod
    def mutate_and_get_payload(cls, root, info, sigle, title, copy_date, copy_place_name, copy_place_latitude, copy_place_longitude, library, signature, scribes, facsimiles):
        # check that codex with the same sigle does not exist
        if not Codex.objects.filter(sigle=sigle).exists():
            return cls(success=False)

        else:
            codex_instance = Codex.objects.create(sigle=sigle, title=title, copy_date=copy_date, copy_place_name=copy_place_name,
                                                  copy_place_latitude=copy_place_latitude, copy_place_longitude=copy_place_longitude, library=library, signature=signature)

            for scribe in scribes:
                # check if author exists
                if Author.objects.filter(name=scribe.name, last_name=scribe.last_name).exists():
                    author_instance = Author.objects.get(name=scribe.name, last_name=scribe.last_name)
                else:
                    # create it
                    author_instance = Author.objects.create(name=scribe.name, last_name=scribe.last_name)
                    author_instance.save()

                codex_instance.authors.add(author_instance)

            for facsimile in facsimiles:
                # check if bibentry exists
                if BibEntry.objects.filter(id=facsimile.id).exists():

                    bibentry_instance = BibEntry.objects.get(id=facsimile.id)
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
        facsimiles = List(BibEntry)

    codex = Field(CodexNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, sigle, title, copy_date, copy_place_name, copy_place_latitude, copy_place_longitude, library, signature, scribes, facsimiles):
        # check that bib exists with id
        if Codex.objects.filter(id=id).exists():
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
                if BibEntry.objects.filter(id=facsimile.id).exists():

                    bibentry_instance = BibEntry.objects.get(id=facsimile.id)
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

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        # check that codex exists with id
        if Codex.objects.filter(id=id).exists():
            codex_instance = Codex.objects.get(id=id)
            codex_instance.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_codex = CreateCodex.Field()
    delete_codex = DeleteCodex.Field()
    update_codex = UpdateCodex.Field()
