import strawberry
import strawberry_django
from strawberry import relay
from typing import  Optional, List
from treeflow.images import models

@strawberry_django.filters.filter(models.Image)
class ImageFilter:
    id: relay.NodeID[str]
    identifier: strawberry.auto

@strawberry_django.type(models.Image)
class Image(relay.Node):

    id: relay.NodeID[str]
    identifier: strawberry.auto
    number: strawberry.auto
    source: strawberry.LazyType['Source', 'treeflow.corpus.types.source']
    previous: Optional['Image']
    next: Optional['Image']
    sections: List[strawberry.LazyType['Section', 'treeflow.corpus.types.section']]


@strawberry_django.input(models.Image)
class ImageInput:
    number: strawberry.auto
    identifier: strawberry.auto
    source: strawberry.auto
    previous: strawberry.auto
    next: strawberry.auto
    sections: strawberry.auto


@strawberry_django.partial(models.Image)
class ImagePartial(strawberry_django.NodeInputPartial):
    id: relay.NodeID[str]
    identifier: strawberry.auto
    number: strawberry.auto
    source: strawberry.auto
    previous: strawberry.auto
    next: strawberry.auto
    sections: strawberry.auto
