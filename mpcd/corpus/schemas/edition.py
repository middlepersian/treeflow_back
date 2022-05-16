from graphene import relay, ObjectType, String, Field, ID, Boolean, List, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Edition
from mpcd.corpus.schemas.author import AuthorInput
from mpcd.corpus.schemas.text_sigle import TextSigleNode
from mpcd.corpus.schemas.bibliography import BibEntryInput


import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class EditionNode(DjangoObjectType):
    class Meta:
        model = Edition
        filter_fields = {'title': ['exact', 'icontains', 'istartswith'],
                         'slug': ['exact', 'icontains', 'istartswith'],
                         'description': ['exact', 'icontains', 'istartswith'],
                         }
        interfaces = (relay.Node,)


# TODO update both create and update Edition methods

class EditionInput(InputObjectType):
    title = String(required=True)
    slug = String(required=True)
    description = String(required=False)
    authors = List(AuthorInput, required=True)
    references = List(BibEntryInput, required=True)
    text_sigle = List(TextSigleNode, required=True)


# Queries
class EditionQuery(ObjectType):
    edition = relay.Node.Field(EditionNode)
    all_editions = DjangoFilterConnectionField(EditionNode)

    @login_required
    def resolve_all_editions(self, info, **kwargs):
        return gql_optimizer.query(Edition.objects.all(), info)

# Mutation


class CreateEdition(relay.ClientIDMutation):
    class Input:
        title = String(required=True)
        slug = String(required=True)
        description = String(required=False)
        authors = List(AuthorInput, required=True)
        references = List(BibEntryInput, required=True)
        text_sigle = List(TextSigleNode, required=True)

    edition = Field(EditionNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        if Edition.get.filter(name=input['title']).exists():
            return cls(errors=['Edition with this title already exists.'])
        else:
            edition = Edition(title=input['title'], slug=input['slug'])
            if input.get('description', None):
                edition.description = input['description']
            edition.save()
            # TODO add authors, references, text_sigle
            return cls(success=True, edition=edition)


class UpdateEdition(relay.ClientIDMutation):
    class Input:
        id = ID()
        title = String(required=True)
        slug = String(required=True)
        description = String(required=False)
        authors = List(AuthorInput, required=True)
        references = List(BibEntryInput, required=True)
        text_sigle = List(TextSigleNode, required=True)

    edition = Field(EditionNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        if Edition.objects.filter(title=input['title']).exists():
            edition = Edition.objects.get(pk=input['id'])
            edition.title = input['title']
            edition.slug = input['slug']
            if input.get('description', None):
                edition.description = input['description']
            edition.save()
            return cls(success=True, edition=edition)
        else:
            return cls(errors=['Edition with this title already exists.'])
        # TODO add authors, references, text_sigle


class DeleteEdition(relay.ClientIDMutation):
    class Input:
        id = ID()

    success = Boolean()

    @classmethod
    @login_required
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
