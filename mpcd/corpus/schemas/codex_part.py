from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.codex_part import CodexPart, CodexPartInput, CodexPartPartial


@gql.type
class Query:
    codex_part: Optional[CodexPart] = gql.django.node()
    codex_parts:  relay.Connection[CodexPart] = gql.django.connection()


@gql.type
class Mutation:
    create_codex_part: CodexPart = gql.django.create_mutation(CodexPartInput)
    update_codex_part: CodexPart = gql.django.update_mutation(CodexPartPartial)
    delete_codex_part: CodexPart = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
