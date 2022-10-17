from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional
from strawberry.lazy_type import LazyType
from mpcd.corpus import models


@gql.django.type(models.Line)
class Line(relay.Node):
    token_line: relay.Connection[LazyType['Token', 'mpcd.corpus.types.token']]

    id: gql.auto
    number: gql.auto
    folio: LazyType['Folio', 'mpcd.corpus.types.folio']
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]
    previous: Optional['Line']
