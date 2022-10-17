
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry.lazy_type import LazyType
from typing import TYPE_CHECKING
from mpcd.corpus import models


@gql.django.type(models.Comment)
class Comment(relay.Node):
    id: gql.auto
    user: LazyType['User', 'mpcd.corpus.types.user']
    text: gql.auto
    created_at: gql.auto
    updated_at: gql.auto
