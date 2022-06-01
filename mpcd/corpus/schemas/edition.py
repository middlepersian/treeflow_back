from graphene import relay, ObjectType, String, Field, ID, Boolean, List, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.corpus.models import Edition, BibEntry
from mpcd.corpus.schemas.text_sigle import TextSigleNode
from mpcd.corpus.schemas.bibliography import BibEntryNode


import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class EditionNode(DjangoObjectType):
    class Meta:
        model = Edition
        filter_fields = {
            'slug': ['exact', 'icontains', 'istartswith'],
            'bib_entry__id': ['exact'],
            'description': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)


# TODO update both create and update Edition methods

class EditionInput(InputObjectType):
    slug = String(required=True)
    bib_entry = ID(required=True)
    description = String(required=False)
    references = List(ID, required=True)
    text_sigles = List(ID, required=True)


# Queries
class Query(ObjectType):
    edition = relay.Node.Field(EditionNode)
    all_editions = DjangoFilterConnectionField(EditionNode)

    @login_required
    def resolve_all_editions(self, info, **kwargs):
        return gql_optimizer.query(Edition.objects.all(), info)

# Mutation


class CreateEdition(relay.ClientIDMutation):
    class Input:
        slug = String(required=True)
        bib_entry = ID(required=True)
        description = String(required=False)
        references = List(ID, required=True)
        text_sigles = List(ID, required=True)

    edition = Field(EditionNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        edition_instance, edition_created = Edition.objects.get_or_create(slug=input.get('slug'))
        if BibEntry.objects.filter(id=input.get('bib_entry')).exists():
            bib_entry_instance = BibEntryNode.objects.get_node_from_global_id(info, input.get('bib_entry'))
            edition_instance.bib_entry = bib_entry_instance

        else:
            return cls(errors=['BibEntry does not exist'])

        for text_sigle_id in input.get('text_sigles'):
            text_sigle_instance = TextSigleNode.get_node_from_global_id(info, text_sigle_id)
            edition_instance.text_sigles.add(text_sigle_instance)

        for reference_id in input.get('references'):
            reference_instance = BibEntryNode.get_node_from_global_id(info, reference_id)
            edition_instance.references.add(reference_instance)

        edition_instance.save()

        return cls(edition=edition_instance, success=True)


class UpdateEdition(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        slug = String(required=True)
        bib_entry = ID(required=True)
        description = String(required=False)
        references = List(ID, required=True)
        text_sigles = List(ID, required=True)

    edition = Field(EditionNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        edition_instance, edition_created = Edition.objects.get(id=input.get('id'))
        edition_instance.slug = input.get('slug')
        if BibEntry.objects.filter(id=input.get('bib_entry')).exists():
            bib_entry_instance = BibEntryNode.objects.get_node_from_global_id(info, input.get('bib_entry'))
            edition_instance.bib_entry = bib_entry_instance

        else:
            return cls(errors=['BibEntry does not exist'])

        for text_sigle_id in input.get('text_sigles'):
            text_sigle_instance = TextSigleNode.get_node_from_global_id(info, text_sigle_id)
            edition_instance.text_sigles.add(text_sigle_instance)

        for reference_id in input.get('references'):
            reference_instance = BibEntryNode.get_node_from_global_id(info, reference_id)
            edition_instance.references.add(reference_instance)

        edition_instance.save()


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
