from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from treeflow.images.types.image import Image, ImageInput, ImagePartial

from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (

    IsAuthenticated,

)


@gql.type
class Query:
    image: Optional[Image] = gql.django.node()
    images:  relay.Connection[Image] = gql.django.connection()


@gql.type
class Mutation:
    create_Image: Image = gql.django.create_mutation(ImageInput, directives=[IsAuthenticated()])
    update_Image: Image = gql.django.update_mutation(ImagePartial, directives=[IsAuthenticated()])
    delete_Image: Image = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
