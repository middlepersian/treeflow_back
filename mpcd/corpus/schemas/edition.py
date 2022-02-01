from graphene import relay, ObjectType, String, Field, ID, Boolean, List, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Edition
from mpcd.corpus.schemas.author import AuthorInput
from mpcd.corpus.schemas.text_sigle import TextSigleNode
from mpcd.corpus.schemas.bibliography import BibEntryInput

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class EditionNode(DjangoObjectType):
    class Meta:
        model = Edition
        filter_fields = {'name': ['exact', 'icontains', 'istartswith'],
                         'slug': ['exact', 'icontains', 'istartswith'],
                         'description': ['exact', 'icontains', 'istartswith'],
                         }
        interfaces = (relay.Node,)


class EditionInput(InputObjectType):
    id = ID()
    name = String()
    slug = String()
    description = String()
    authors = List(AuthorInput)
    references = List(BibEntryInput)
    text_sigle = List(TextSigleNode)


# Queries
class EditionQuery(ObjectType):
    edition = relay.Node.Field(EditionNode)
    all_editions = DjangoFilterConnectionField(EditionNode)

# Mutation


class CreateEdition(relay.ClientIDMutation):
    class Input:
        id = ID()
        name = String()
        slug = String()
        description = String()
        authors = List(AuthorInput)
        references = List(BibEntryInput)
        text_sigle = List(TextSigleNode)

    edition = Field(EditionNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if Edition.get.filter(name=input['name']).exists():
            return cls(errors=['Edition with this name already exists.'])
        else:
            edition = Edition(name=input['name'], slug=input['slug'], description=input['description'])
            edition.save()
            # TODO add authors, references, text_sigle
            return cls(success=True, edition=edition)


class UpdateEdition(relay.ClientIDMutation):
    class Input:
        id = ID()
        name = String()
        slug = String()
        description = String()
        authors = List(AuthorInput)
        references = List(BibEntryInput)
        text_sigle = List(TextSigleNode)

    edition = Field(EditionNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if Edition.objects.filter(name=input['name']).exists():
            edition = Edition.objects.get(pk=input['id'])
            edition.name = input['name']
            edition.slug = input['slug']
            edition.description = input['description']
            edition.save()
            return cls(success=True, edition=edition)
        else:
            return cls(errors=['Edition with this name already exists.'])
        # TODO add authors, references, text_sigle


class DeleteEdition(relay.ClientIDMutation):
    class Input:
        id = ID()

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if Edition.objects.filter(pk=input['id']).exists():
            edition = Edition.objects.get(pk=input['id'])
            edition.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation (ObjectType):
    create_edition = CreateEdition.Field()
    update_edition = UpdateEdition.Field()
    delete_edition = DeleteEdition.Field()
