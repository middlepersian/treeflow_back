from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from treeflow.images.types.facsimile import Facsimile, FacsimileInput, FacsimilePartial


from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (
    HasObjPerm,
    HasPerm,
    IsAuthenticated,
    IsStaff,
    IsSuperuser,
)


@gql.type
class Query:
    facsimile: Optional[Facsimile] = gql.django.node(directives=[IsAuthenticated()])
    facsimiles:  relay.Connection[Facsimile] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:
    create_facsimile: Facsimile = gql.django.create_mutation(FacsimileInput, directives=[IsAuthenticated()])
    update_facsimile: Facsimile = gql.django.update_mutation(FacsimilePartial, directives=[IsAuthenticated()])
    delete_facsimile: Facsimile = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation,
                    extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
