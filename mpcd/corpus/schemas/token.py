from typing import Optional
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension


from mpcd.corpus.types.token import Token, TokenInput, TokenPartial


@gql.type
class Query:
    token: Optional[Token] = gql.django.node()
    tokens: relay.Connection[Token] = gql.django.connection()


@gql.type
class Mutation:
    create_token: Token = gql.django.create_mutation(TokenInput)
    update_token: Token = gql.django.update_mutation(TokenPartial)
    delete_token: Token = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
