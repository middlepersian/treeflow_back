import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from treeflow.corpus.types.dependency import Dependency, DependencyPartial, DependencyInput, DeprelList
from treeflow.corpus.enums.deprel import Deprel


from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (
    HasObjPerm,
    HasPerm,
    IsAuthenticated,
    IsStaff,
    IsSuperuser,
)


@gql.type
class Query:
    dependency: Optional[Dependency] = gql.django.node()
    dependencies:  relay.Connection[Dependency] = gql.django.connection()

    @strawberry.field
    def deprel_list(self, info) -> DeprelList:
        dep_list = [dep.value for dep in Deprel]
        return DeprelList(dep=dep_list)


@gql.type
class Mutation:
    create_dependency: Dependency = gql.django.create_mutation(DependencyInput, directives=[IsAuthenticated()])
    update_dependency: Dependency = gql.django.update_mutation(DependencyPartial, directives=[IsAuthenticated()])
    delete_dependency: Dependency = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
