from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from mpcd.corpus.types.dependency import Dependency, DependencyPartial, DependencyInput


@gql.type
class Query:
    dependency: Optional[Dependency] = gql.django.node()
    dependencies:  relay.Connection[Dependency] = gql.django.connection()


@gql.type
class Mutation:
    create_dependency: Dependency = gql.django.create_mutation(DependencyInput)
    update_dependency: Dependency = gql.django.update_mutation(DependencyPartial)
    delete_dependency: Dependency = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
