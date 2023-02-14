
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import  Optional
from treeflow.corpus import models


@gql.django.type(models.Dependency)
class Dependency(relay.Node):

    token_dependencies: relay.Connection[gql.LazyType['Token', 'treeflow.corpus.types.token']]

    id: relay.GlobalID
    head:  Optional[gql.LazyType['Token', 'treeflow.corpus.types.token']]
    head_number: Optional[float]
    rel: gql.auto
    producer: gql.auto


@gql.django.input(models.Dependency)
class DependencyInput:
    head:  gql.auto
    head_number: gql.auto
    rel: gql.auto
    producer: gql.auto


@gql.django.partial(models.Dependency)
class DependencyPartial(gql.NodeInputPartial):
    id: relay.GlobalID
    head:  gql.auto
    head_number: gql.auto
    rel: gql.auto
    producer: gql.auto
