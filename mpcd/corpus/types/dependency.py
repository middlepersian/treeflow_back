
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING
from strawberry.lazy_type import LazyType
from mpcd.corpus import models


@gql.django.type(models.Dependency)
class Dependency(relay.Node):

    token_syntactic_annotation: relay.Connection[LazyType['Token', 'mpcd.corpus.types.token']]

    id: gql.auto
    head:  LazyType['Token', 'mpcd.corpus.types.token']
    rel: gql.auto
    producer: gql.auto
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]
