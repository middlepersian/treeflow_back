from graphene import relay, ObjectType, Field, ID, Boolean, List, InputObjectType, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import BibEntry

import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class BibEntryNode(DjangoObjectType):
    class Meta:
        model = BibEntry
        filter_fields = {
            'key': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)


class BibEntryInput(InputObjectType):
    key = String(required=True)


# Queries

class Query(ObjectType):
    bibentry = relay.Node.Field(BibEntryNode)
    all_bibentries = DjangoFilterConnectionField(BibEntryNode)

    @login_required
    def resolve_all_bibentries(self, info, **kwargs):
        return gql_optimizer.query(BibEntry.objects.all(), info)

# Mutations


class CreateBibEntry(relay.ClientIDMutation):
    class Input:
        key = String(required=True)

    bibentry = Field(BibEntryNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.error("input: {}".format(input))

        bibentry_instance, bibentry_created = BibEntry.objects.get_or_create(key=input['key'])

        return cls(bibentry=bibentry_instance, success=True)


class UpdateBibEntry(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        key = String(required=True)

    bibentry = Field(BibEntryNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):

        if BibEntry.objects.filter(pk=from_global_id(id)[1]).exists():
            bibentry_instance = BibEntry.objects.get(pk=from_global_id(id)[1])
        else:
            return cls(success=False, errors=['BibEntry does not exist'])

        bibentry_instance.key = input['key']

        bibentry_instance.save()
        return cls(bibentry=bibentry_instance, success=True)


class DeleteBibEntry(relay.ClientIDMutation):

    success = Boolean()

    class Input:
        id = ID(required=True)

    @classmethod
    @login_required
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
