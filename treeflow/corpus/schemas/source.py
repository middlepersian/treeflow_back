from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from treeflow.corpus.types.source import Source, SourceInput, SourcePartial


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
    source: Optional[Source] = gql.django.node(directives=[IsAuthenticated()])
    sources:  relay.Connection[Source] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:
    create_source: Source = gql.django.create_mutation(SourceInput, directives=[IsAuthenticated()])
    update_source: Source = gql.django.update_mutation(SourcePartial, directives=[IsAuthenticated()])
    delete_source: Source = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
