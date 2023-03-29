import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import  Optional, List
from treeflow.corpus import models
from treeflow.corpus.enums.deprel import Deprel


@gql.django.type(models.Dependency)
class Dependency(relay.Node):

    token_dependencies: relay.Connection[gql.LazyType['Token', 'treeflow.corpus.types.token']]

    id: relay.GlobalID
    token: Optional[gql.LazyType['Token', 'treeflow.corpus.types.token']]
    head:  Optional[gql.LazyType['Token', 'treeflow.corpus.types.token']]
    head_number: Optional[float]
    rel: Deprel
    producer: gql.auto


@gql.django.input(models.Dependency)
class DependencyInput:
    token: relay.GlobalID
    head:  relay.GlobalID
    head_number: gql.auto
    rel: Deprel
    producer: gql.auto


@gql.django.partial(models.Dependency)
class DependencyPartial(gql.NodeInputPartial):
    id: relay.GlobalID
    token: relay.GlobalID
    head:  relay.GlobalID
    head_number: gql.auto
    rel: Deprel
    producer: gql.auto


@strawberry.type
class DeprelList:
    dep: List[Deprel]