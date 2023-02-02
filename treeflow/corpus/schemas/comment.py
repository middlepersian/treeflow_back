from typing import Optional
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension


from treeflow.corpus.types.comment import Comment, CommentInput, CommentPartial

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
    comment: Optional[Comment] = gql.django.node(directives=[IsAuthenticated()])
    comments: relay.Connection[Comment] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:
    create_comment: Comment = gql.django.create_mutation(CommentInput, directives=[IsAuthenticated()])
    update_comment: Comment = gql.django.update_mutation(CommentPartial, directives=[IsAuthenticated()])
    delete_comment: Comment = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
