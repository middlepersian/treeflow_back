from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.line import Line, LineInput, LinePartial


@gql.type
class Query:
    line: Optional[Line] = gql.django.node()
    lines:  relay.Connection[Line] = gql.django.connection()


@gql.type
class Mutation:
    create_line: Line = gql.django.create_mutation(LineInput)
    update_line: Line = gql.django.update_mutation(LinePartial)
    delete_line: Line = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
