from typing import List
from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from mpcd.corpus.types.comment import Comment, CommentInput, CommentInputPartial


@gql.type
class Query:
    comments: List[Comment] = gql.django.field()


@gql.type
class Mutation:
    create_model: Comment = gql.django.create_mutation(CommentInput)
    update_model: Comment = gql.django.update_mutation(CommentInputPartial)
    delete_model: Comment = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
