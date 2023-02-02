from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import  Optional
from treeflow.images import models



@gql.django.type(models.Image)
class Image(relay.Node):

    id: relay.GlobalID
    number: gql.auto
    facsimile: gql.LazyType['Facsimile', 'treeflow.images.types.facsimile']
    previous: Optional['Image']
    next: Optional['Image']



@gql.django.input(models.Image)
class ImageInput:
    number: gql.auto
    facsimile: gql.auto
    previous: gql.auto
    next: gql.auto


@gql.django.partial(models.Image)
class ImagePartial(gql.NodeInputPartial):
    id: relay.GlobalID
    number: gql.auto
    facsimile: gql.auto
    previous: gql.auto
    next: gql.auto
