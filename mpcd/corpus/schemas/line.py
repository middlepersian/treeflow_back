from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.line import Line, LineInput, LinePartial

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
    line: Optional[Line] = gql.django.node(directives=[IsAuthenticated()])
    lines:  relay.Connection[Line] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:
    create_line: Line = gql.django.create_mutation(LineInput, directives=[IsAuthenticated()])
    update_line: Line = gql.django.update_mutation(LinePartial, directives=[IsAuthenticated()])
    delete_line: Line = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
