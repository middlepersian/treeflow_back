from graphene import relay, InputObjectType, String, Field, ObjectType, List, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Resource, Author
from mpcd.corpus.schemas.author import AuthorInput


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
    authors = List(AuthorInput)
    description = String()
    project = String()
    reference = String()


class Query(ObjectType):
    resource = relay.Node.Field(ResourceNode)
    all_resource = DjangoFilterConnectionField(ResourceNode)


# Mutations

class CreateResource(relay.ClientIDMutation):
    class Input:
        authors = List(AuthorInput)
        description = String()
        project = String()
        reference = String()

    resource = Field(ResourceNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, authors, description, project, reference):

        if Resource.objects.filter(project=project, description=description).exists():
            return cls(success=False)
        else:
            resource = Resource.objects.create(description=description, project=project, reference=reference)
            for author in authors:
                # check if author exists
                if Author.objects.filter(name=author.name, last_name=author.last_name).exists():
                    author_instance = Author.objects.get(name=author.name, last_name=author.last_name)
                else:
                    # create it
                    author_instance = Author.objects.create(name=author.name, last_name=author.last_name)
                    author_instance.save()
                resource.authors.add(author_instance)
            resource.save()
            return cls(resource=resource, success=True)


class UpdateResource(relay.ClientIDMutation):
    class Input:
        id = ID()
        authors = List(AuthorInput)
        description = String()
        project = String()
        reference = String()

    resource = Field(ResourceNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, authors, description, project, reference):
        resource = Resource.objects.get(pk=from_global_id(id)[1])
        if Resource.objects.filter(project=project, description=description).exists():
            return cls(success=False)
        else:
            resource.description = description
            resource.project = project
            resource.reference = reference
            resource.authors.clear()
            for author in authors:
                # check if author exists
                if Author.objects.filter(name=author.name, last_name=author.last_name).exists():
                    author_instance = Author.objects.get(name=author.name, last_name=author.last_name)
                else:
                    # create it
                    author_instance = Author.objects.create(name=author.name, last_name=author.last_name)
                    author_instance.save()
                resource.authors.add(author_instance)
            resource.save()
            return cls(resource=resource, success=True)


class DeleteResource(relay.ClientIDMutation):
    class Input:
        id = ID()

    resource = Field(ResourceNode)
    success = Boolean()

    @classmethod
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
