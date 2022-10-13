from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from strawberry.lazy_type import LazyType
from typing import List, TYPE_CHECKING, Optional
from mpcd.corpus import models
if TYPE_CHECKING:
    from mpcd.corpus.types.user import User


@gql.django.type(models.TokenComment)
class TokenComment(relay.Node):
    id: gql.auto
    user: LazyType['User', 'mpcd.corpus.types.user']
    text: gql.auto
    created_at: gql.auto
    updated_at: gql.auto
    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]
