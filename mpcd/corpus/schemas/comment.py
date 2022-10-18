from typing import Optional
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension


from mpcd.corpus.types.comment import Comment, CommentInput, CommentPartial


@gql.type
class Query:
    comment: Optional[Comment] = gql.django.node()
    comments: relay.Connection[Comment] = gql.django.connection()


@gql.type
class Mutation:
    create_comment: Comment = gql.django.create_mutation(CommentInput)
    update_comment: Comment = gql.django.update_mutation(CommentPartial)
    delete_comment: Comment = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
