from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.codex_part import CodexPart


@gql.type
class Query:
    codex_part: Optional[CodexPart] = gql.django.node()
    codex_parts:  relay.Connection[CodexPart] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
