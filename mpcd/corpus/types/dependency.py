
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional
from strawberry.lazy_type import LazyType
from mpcd.corpus import models
from mpcd.corpus.types.comment import CommentPartial, CommentInput


@gql.django.type(models.Dependency)
class Dependency(relay.Node):

    token_syntactic_annotation: relay.Connection[LazyType['Token', 'mpcd.corpus.types.token']]

    id: gql.auto
    head:  LazyType['Token', 'mpcd.corpus.types.token']
    rel: gql.auto
    producer: gql.auto
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]


@gql.django.input(models.Dependency)
class DependencyInput:
    head:  gql.auto
    rel: gql.auto
    producer: gql.auto
    comments:  Optional[List[CommentInput]]


@gql.django.partial(models.Dependency)
class DependencyPartial(gql.NodeInputPartial):
    id: gql.auto
    head:  gql.auto
    rel: gql.auto
    producer: gql.auto
    comments:   Optional[gql.ListInput[CommentPartial]]
