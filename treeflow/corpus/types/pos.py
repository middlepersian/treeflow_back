import strawberry
import strawberry_django
from strawberry import relay
from typing import List, Optional

from treeflow.corpus import models

@strawberry_django.type(models.POS)
class POS(relay.Node):
    id: relay.NodeID[str]
    token : strawberry.LazyType['Token', 'treeflow.corpus.types.token']
    pos: strawberry.auto
    type: strawberry.auto

@strawberry_django.input(models.POS)
class POSInput:
    token : strawberry.auto
    pos: strawberry.auto
    type: strawberry.auto

@strawberry_django.partial(models.POS)
class POSPartial:
    id: relay.GlobalID
    token: strawberry.auto
    pos: strawberry.auto
    type: strawberry.auto
