from typing import Optional
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from mpcd.corpus.types.token_comment import TokenComment, TokenCommentInput, TokenCommentPartial


@gql.type
class Query:
    token_comment: Optional[TokenComment] = gql.django.node()
    token_comments:  relay.Connection[TokenComment] = gql.django.connection()


@gql.type
class Mutation:
    create_token_comment: TokenComment = gql.django.create_mutation(TokenCommentInput)
    update_token_comment: TokenComment = gql.django.update_mutation(TokenCommentPartial)
    delete_token_comment: TokenComment = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
