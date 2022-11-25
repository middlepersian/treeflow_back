from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import TYPE_CHECKING, Annotated, Optional
from mpcd.corpus import models

if TYPE_CHECKING:
    from .user import User


@gql.django.type(models.Comment)
class Comment(relay.Node):
    id: relay.GlobalID
    user: Optional[gql.LazyType['User', 'mpcd.corpus.types.user']]
    text: gql.auto
    created_at: gql.auto
    updated_at: gql.auto


@gql.django.input(models.Comment)
class CommentInput:
    id: relay.GlobalID
    user: gql.auto
    text: gql.auto


@gql.django.partial(models.Comment)
class CommentPartial(gql.NodeInputPartial):
    id: relay.GlobalID
    user: gql.auto
    text: gql.auto
