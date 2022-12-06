from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.codex_part import CodexPart, CodexPartInput, CodexPartPartial

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
    codex_part: Optional[CodexPart] = gql.django.node(directives=[IsAuthenticated()])
    codex_parts:  relay.Connection[CodexPart] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:
    create_codex_part: CodexPart = gql.django.create_mutation(CodexPartInput, directives=[IsAuthenticated()])
    update_codex_part: CodexPart = gql.django.update_mutation(CodexPartPartial, directives=[IsAuthenticated()])
    delete_codex_part: CodexPart = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
