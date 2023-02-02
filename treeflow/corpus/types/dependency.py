
from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import Annotated, List, TYPE_CHECKING, Optional
from treeflow.corpus import models

if TYPE_CHECKING:
    from .token import Token
    from .comment import Comment


@gql.django.type(models.Dependency)
class Dependency(relay.Node):

    token_syntactic_annotation: relay.Connection[gql.LazyType['Token', 'treeflow.corpus.types.token']]

    id: relay.GlobalID
    head:  gql.LazyType['Token', 'treeflow.corpus.types.token']
    rel: gql.auto
    producer: gql.auto


@gql.django.input(models.Dependency)
class DependencyInput:
    head:  gql.auto
    rel: gql.auto
    producer: gql.auto


@gql.django.partial(models.Dependency)
class DependencyPartial(gql.NodeInputPartial):
    id: relay.GlobalID
    head:  gql.auto
    rel: gql.auto
    producer: gql.auto
