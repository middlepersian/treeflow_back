from graphene import relay, ObjectType, String, InputObjectType, ID, List, Field, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id


import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


from mpcd.corpus.models import Source


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class SourceNode(DjangoObjectType):
    class Meta:
        model = Source
        filter_fields = {
            'identifier': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains', 'istartswith'], 'bib_entry__id': ['exact']}


class Query(ObjectType):
    source = relay.Node.Field(SourceNode)
    all_source = DjangoFilterConnectionField(SourceNode)

    @login_required
    def resolve_all_sources(self, info, **kwargs):
        return gql_optimizer.query(Source.objects.all(), info)


class SourceInput(InputObjectType):
    identifier = String(required=True)
    description = String(required=False)
    bib_entry = ID(required=True)


class CreateSource(relay.ClientIDMutation):
    class Input:
        source_input = SourceInput(required=True)

    source = Field(SourceNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        source_input = input.get('source_input')
        source_obj, source_created = Source.objects.get_or_create(identifier=source_input.identifier,
                        description=source_input.description, bib_entry=source_input.bib_entry)

        return cls(source=source_obj, success=True, errors=None)


class UpdateSource(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        source_input = SourceInput(required=True)

    source = Field(SourceNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        if Source.objects.filter(pk=from_global_id(input['id'])[1]).exists():
            source = Source.objects.get(pk=from_global_id(input['id'])[1])
            source_input = input.get('source_input')
            source.identifier = source_input.identifier
            source.description = source_input.description
            source.bib_entry = source_input.bib_entry
            source.save()
            return cls(source=source, success=True, errors=None)

        else:
            return cls(source=None, success=False, errors=['Source ID not found'])


class DeleteSource(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        if Source.objects.filter(pk=from_global_id(input['id'])[1]).exists():
            source = Source.objects.get(pk=from_global_id(input['id'])[1])
            source.delete()
            return cls(success=True, errors=None)

        else:
            return cls(success=False, errors=['Source ID not found'])


class Mutation(ObjectType):
    create_source = CreateSource.Field()
    update_source = UpdateSource.Field()
    delete_source = DeleteSource.Field()

