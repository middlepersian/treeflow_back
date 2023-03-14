from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import  Optional, List
from treeflow.images import models

@gql.django.filters.filter(models.Image)
class ImageFilter:
    id: relay.GlobalID
    identifier: gql.auto

@gql.django.type(models.Image)
class Image(relay.Node):

    id: relay.GlobalID
    identifier: gql.auto
    number: gql.auto
    source: gql.LazyType['Source', 'treeflow.corpus.types.source']
    previous: Optional['Image']
    next: Optional['Image']
    sections: List[gql.LazyType['Section', 'treeflow.corpus.types.section']]


@gql.django.input(models.Image)
class ImageInput:
    number: gql.auto
    identifier: gql.auto
    source: gql.auto
    previous: gql.auto
    next: gql.auto
    sections: gql.auto


@gql.django.partial(models.Image)
class ImagePartial(gql.NodeInputPartial):
    id: relay.GlobalID
    identifier: gql.auto
    number: gql.auto
    source: gql.auto
    previous: gql.auto
    next: gql.auto
    sections: gql.auto
