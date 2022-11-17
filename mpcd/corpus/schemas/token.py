from typing import Optional, cast
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from strawberry.types.info import Info


from mpcd.corpus.types.token import Token, TokenInput, TokenPartial
import mpcd.corpus.models as models


@gql.type
class Query:
    token: Optional[Token] = gql.django.node()
    tokens: relay.Connection[Token] = gql.django.connection()


@gql.type
class Mutation:
    create_token: Token = gql.django.create_mutation(TokenInput)
    update_token: Token = gql.django.update_mutation(TokenPartial)
    delete_token: Token = gql.django.delete_mutation(gql.NodeInput)

    @gql.django.mutation
    def join_tokens(self, 
                    info,
                    current: relay.GlobalID,
                    previous: relay.GlobalID,
                    ) -> Token:

        current_token = current.resolve_node(info)    
        previous_token = previous.resolve_node(info)        
        current_token.previous = previous_token
        current_token.save()
        return current_token


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
