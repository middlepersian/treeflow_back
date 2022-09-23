from typing import List
from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from mpcd.corpus.types.token import Token, TokenInput, TokenInputPartial


@gql.type
class Query:
    tokens: List[Token] = gql.django.field()


@gql.type
class Mutation:
    create_model: Token = gql.django.create_mutation(TokenInput)
    update_model: Token = gql.django.update_mutation(TokenInputPartial)
    delete_model: Token = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
