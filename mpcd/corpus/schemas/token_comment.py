from typing import Optional
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from mpcd.corpus.types.token_comment import TokenComment, TokenCommentInput, TokenCommentPartial

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
    token_comment: Optional[TokenComment] = gql.django.node(directives=[IsAuthenticated()])
    token_comments:  relay.Connection[TokenComment] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:
    create_token_comment: TokenComment = gql.django.create_mutation(TokenCommentInput, directives=[IsAuthenticated()])
    update_token_comment: TokenComment = gql.django.update_mutation(TokenCommentPartial, directives=[IsAuthenticated()])
    delete_token_comment: TokenComment = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
