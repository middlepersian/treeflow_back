
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING
from strawberry.lazy_type import LazyType
from mpcd.corpus import models

if TYPE_CHECKING:
    from mpcd.corpus.types.comment import Comment
    from mpcd.corpus.types.token import Token
    from strawberry.lazy_type import LazyType


@gql.django.type(models.Dependency)
class Dependency(relay.Node):
    id: gql.auto
    head:  LazyType['Token', 'mpcd.corpus.types.token']
    rel: gql.auto
    producer: gql.auto
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]
