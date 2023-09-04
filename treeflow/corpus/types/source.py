
import strawberry
import strawberry_django
from strawberry import relay
from typing import Optional, List

from treeflow.corpus import models


@strawberry_django.type(models.Source)
class Source(relay.Node):

    image_source: List[strawberry.LazyType['Image',  'treeflow.images.types.image']] = strawberry_django.field()


    id: relay.NodeID[str]
    type: strawberry.auto
    identifier: strawberry.auto
    description: strawberry.auto
    references: List[strawberry.LazyType['BibEntry', 'treeflow.corpus.types.bibliography']]
    sources: Optional[List['Source']]


@strawberry_django.input(models.Source)
class SourceInput:

    type: strawberry.auto
    identifier: strawberry.auto
    description: strawberry.auto
    references: strawberry.auto
    sources: strawberry.auto


@strawberry_django.partial(models.Source)
class SourcePartial:
    
    id: relay.GlobalID
    type: strawberry.auto
    identifier: strawberry.auto
    description: strawberry.auto
    references: strawberry.auto
    sources: strawberry.auto
