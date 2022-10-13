from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from strawberry.lazy_type import LazyType
from typing import List, TYPE_CHECKING
from mpcd.corpus import models

if TYPE_CHECKING:
    from mpcd.corpus.types.comment import Comment
    from mpcd.corpus.types.facsimile import Facsimile


@gql.django.type(models.Line)
class Folio(relay.Node):
    id: gql.auto
    number: gql.auto
    facsimile: LazyType['Facsimile', 'mpcd.corpus.types.facsimile']
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]
    previous: 'Folio'