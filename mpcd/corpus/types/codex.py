from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from strawberry.lazy_type import LazyType
from typing import List, TYPE_CHECKING
from mpcd.corpus import models

if TYPE_CHECKING:
    from mpcd.corpus.types.comment import Comment


@gql.django.type(models.Codex)
class Codex(relay.Node):
    sigle: gql.auto
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]
