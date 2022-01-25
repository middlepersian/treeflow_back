from graphene import relay, ObjectType, String, Field, ID, Boolean, List, Int, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.corpus.models import Token, Feature, FeatureValue, MorphologicalAnnotation, Pos, Dependency
from mpcd.corpus.schemas import MorphologicalAnnotationNode, MorphologicalAnnotationInput
from mpcd.corpus.schemas import PosNode, PosInput
from mpcd.corpus.schemas import DependencyNode, DependencyInput
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class DependencyNode(DjangoObjectType):
    class Meta:
        model = Dependency
        filter_fields = {'rel': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)

    interfaces = (relay.Node,)


class DependencyInput(InputObjectType):
    head = Int()
    rel = String()

# Queries


class Query(ObjectType):
    dependency = relay.Node.Field(DependencyNode)
    all_dependencies = DjangoFilterConnectionField(DependencyNode)


# Mutations
class CreateDependency(relay.ClientIDMutation):
    class Input:
        head = Int(required=True)
        rel = String(required=True)

    dependency = Field(DependencyNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, head, rel):
        # check that dependency does not exist
        if Dependency.objects.filter(head=head, rel=rel).exists():
            return cls(success=False)

        else:
            dependency_instance = Dependency.objects.create(head=head, rel=rel)

            return cls(dependency=dependency_instance, success=True)

class UpdateDependency(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        head = Int()
        rel = String()

    dependency = Field(DependencyNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, head, rel):
        # check that dependency does not exist
        if Dependency.objects.filter(id=id).exists():
            dependency_instance = Dependency.objects.get(id=id)
            dependency_instance.head = head
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
    def mutate_and_get_payload(cls, root, info, id):
        # check that dependency does not exist
        if Dependency.objects.filter(id=id).exists():
            dependency_instance = Dependency.objects.get(id=id)
            dependency_instance.delete()
            return cls(dependency=dependency_instance, success=True)

        else:
            return cls(success=False)            

class Mutation(ObjectType):
    create_dependency = CreateDependency.Field()
    update_dependency = UpdateDependency.Field()
    delete_dependency = DeleteDependency.Field()