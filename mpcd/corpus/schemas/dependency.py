from mpcd.corpus.schemas.dependency_enum import DependencyEnum
from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

from mpcd.corpus.models import Dependency, Token
from graphql_jwt.decorators import login_required


import graphene_django_optimizer as gql_optimizer

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class DependencyNode(DjangoObjectType):
    class Meta:
        model = Dependency
        filter_fields = {
            'head': ['exact'],
            'rel': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)

    interfaces = (relay.Node,)


class DependencyInput(InputObjectType):
    head = ID(required=True)
    rel = DependencyEnum(required=True)

# Queries


class Query(ObjectType):
    dependency = relay.Node.Field(DependencyNode)
    all_dependencies = DjangoFilterConnectionField(DependencyNode)

    @login_required
    def resolve_all_dependencies(self, info, **kwargs):
        return gql_optimizer.query(Dependency.objects.all(), info)


# Mutations
class CreateDependency(relay.ClientIDMutation):
    class Input:
        head = ID(required=True)
        rel = DependencyEnum(required=True)

    dependency = Field(DependencyNode)
    success = Boolean()
    errors = True

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, head, rel):
        # check that dependency does not exist
        if Dependency.objects.filter(head=head, rel=rel).exists():
            return cls(success=False, errors=True, dependency=None)

        else:
            local_head = Token.objects.get(id=from_global_id(head)[1])
            dependency_instance = Dependency.objects.get_or_create(head=local_head, rel=rel)
            dependency_instance.save()

            return cls(dependency=dependency_instance, success=True, errors=False)


class UpdateDependency(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        head = ID(required=True)
        rel = DependencyEnum(required=True)

    dependency = Field(DependencyNode)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, id, head, rel):
        # check that dependency does not exist
        if Dependency.objects.filter(pk=from_global_id(id)[1]).exists():
            dependency_instance = Dependency.objects.get(pk=from_global_id(id)[1])
            # get head
            local_head = Token.objects.get(pk=from_global_id(head)[1])
            dependency_instance.head = local_head
            dependency_instance.rel = rel
            dependency_instance.save()
            return cls(dependency=dependency_instance, success=True)

        else:
            return cls(success=False)


class DeleteDependency(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    dependency = Field(DependencyNode)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, id):
        # check that dependency does exist
        if Dependency.objects.filter(pk=from_global_id(id)[1]).exists():
            dependency_instance = Dependency.objects.get(pk=from_global_id(id)[1])
            dependency_instance.delete()
            return cls(dependency=dependency_instance, success=True)

        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_dependency = CreateDependency.Field()
    update_dependency = UpdateDependency.Field()
    delete_dependency = DeleteDependency.Field()
