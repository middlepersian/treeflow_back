
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from mpcd.corpus import models
from mpcd.corpus.types import User

@gql.django.type(models.Comment)
class Comment:
    id: gql.auto
    user: 'User'
    text: gql.auto
    created_at: gql.auto
    updated_at: gql.auto


@gql.django.input(models.Comment)
class CommentInput:
    text: gql.auto


@gql.django.partial(models.Comment)
class CommentInputPartial(gql.NodeInput):
    text: gql.auto


