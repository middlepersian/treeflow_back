from distutils import errors
from graphene import relay, InputObjectType, String, Field, ObjectType, List, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Resource, Author
from mpcd.corpus.schemas.author import AuthorInput

import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class ResourceNode(DjangoObjectType):
    class Meta:
        model = Resource
        filter_fields = {'authors': ['exact', 'icontains', 'istartswith'],
                         'description': ['exact', 'icontains', 'istartswith'],
                         'project': ['exact', 'icontains', 'istartswith'],
                         'reference': ['exact', 'icontains', 'istartswith'], }
        interfaces = (relay.Node,)


class ResourceInput(InputObjectType):
    project = String(required=True)
    authors = List(AuthorInput, required=True)
    description = String(required=False)
    reference = String(required=False)


class Query(ObjectType):
    resource = relay.Node.Field(ResourceNode)
    all_resources = DjangoFilterConnectionField(ResourceNode)

    @login_required
    def resolve_all_resources(self, info, **kwargs):
        return gql_optimizer.query(Resource.objects.all(), info)


# Mutations

class CreateResource(relay.ClientIDMutation):
    class Input:
        project = String(required=True)
        authors = List(AuthorInput, required=True)
        description = String(required=False)
        reference = String(required=False)

    resource = Field(ResourceNode)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):

        resource_obj, resource_created = Resource.objects.get_or_create(project=input.get('project'))

        if input.get('description'):
            resource_obj.description = input.get('description')

        if input.get('reference'):
            resource_obj.reference = input.get('reference')

        for author in input.get('authors'):
            author_obj, author_created = Author.objects.get_or_create(
                name=author.get('name'), last_name=author.get('last_name'))
            resource_obj.authors.add(author_obj)

        resource_obj.save()
        return cls(resource=resource_obj, success=True)


class UpdateResource(relay.ClientIDMutation):
    class Input:
        id = ID()
        project = String(required=True)
        authors = List(AuthorInput, required=True)
        description = String(required=False)
        reference = String(required=False)

    resource = Field(ResourceNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):

        if Resource.Resource.objects.get(pk=from_global_id(id)[1]).exists():
            resource = Resource.objects.get(pk=from_global_id(id)[1])
            resource.project = input.get('project')

            if input.get('description'):
                resource.description = input.get('description')
            if input.get('reference'):
                resource.reference = input.get('reference')

            # clear all authors
            resource.authors.clear()
            for author in input.get('authors'):
                author_obj, author_created = Author.objects.get_or_create(
                    name=author.get('name'), last_name=author.get('last_name'))
                resource.authors.add(author_obj)

            resource.save()
            return cls(resource=resource, success=True, errors=None)

        else:
            return cls(resource=None, success=False, errors=['Resource ID not valid'])


class DeleteResource(relay.ClientIDMutation):
    class Input:
        id = ID()

    resource = Field(ResourceNode)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, id):
        if Resource.objects.filter(pk=from_global_id(id)[1]).exists():
            resource = Resource.objects.get(pk=from_global_id(id)[1])
            resource.delete()
            return cls(resource=resource, success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_resource = CreateResource.Field()
    update_resource = UpdateResource.Field()
    delete_resource = DeleteResource.Field()
