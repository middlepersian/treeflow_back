from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING
from strawberry.lazy_type import LazyType
from mpcd.corpus import models

if TYPE_CHECKING:
    from mpcd.corpus.types.comment import Comment
    from mpcd.corpus.types.folio import Folio


@gql.django.type(models.Line)
class Line:
    id: gql.auto
    number: gql.auto
    folio: LazyType['Folio', 'mpcd.corpus.types.folio']
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]
    previous: 'Line'
