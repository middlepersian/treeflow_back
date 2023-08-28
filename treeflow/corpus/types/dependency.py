import strawberry
import strawberry_django
from strawberry import relay
from typing import  Optional, List
from treeflow.corpus import models
from treeflow.corpus.enums.deprel import Deprel

@strawberry_django.type(models.Dependency)
class Dependency(relay.Node):

    token_dependencies: List[strawberry.LazyType['Token', 'treeflow.corpus.types.token']] = strawberry_django.field()

    id: relay.NodeID[str]
    token: Optional[strawberry.LazyType['Token', 'treeflow.corpus.types.token']]
    head:  Optional[strawberry.LazyType['Token', 'treeflow.corpus.types.token']]
    head_number: Optional[float]
    rel: Deprel
    producer: strawberry.auto


@strawberry_django.input(models.Dependency)
class DependencyInput:
    token: strawberry.auto
    head:  strawberry.auto
    head_number: strawberry.auto
    rel: Optional[Deprel]
    producer: strawberry.auto


@strawberry_django.partial(models.Dependency)
class DependencyPartial:
    id: relay.GlobalID
    token: strawberry.auto
    head:  strawberry.auto
    head_number: strawberry.auto
    rel: Deprel
    producer: strawberry.auto


@strawberry.type
class DeprelList:
    dep: List[Deprel]