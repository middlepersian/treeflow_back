from asgiref.sync import sync_to_async
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List
from mpcd.corpus.models import Comment


async def get_all_posts(root, info) -> List[Comment]:
    get_comments = sync_to_async(lambda: Comment.objects.all())
    return await get_comments()


@gql.django.type(Comment)
class CommentType(gql.Node):
    text: gql.auto


@gql.django.input(Comment)
class CommentInput:
    text: gql.auto


@gql.django.partial(Comment)
class CommentInputPartial(gql.NodeInput):
    text: gql.auto


@gql.type
class Query:
    comments: List[CommentType] = gql.django.field(resolver=get_all_posts)

@gql.type
class Mutation:
    create_model : CommentType = gql.django.create_mutation(CommentInput)
    update_model : CommentType = gql.django.update_mutation(CommentInputPartial)
    delete_model : CommentType = gql.django.delete_mutation(gql.NodeInput)


