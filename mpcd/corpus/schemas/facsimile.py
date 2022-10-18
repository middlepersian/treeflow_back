from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from mpcd.corpus.types.facsimile import Facsimile, FacsimileInput, FacsimilePartial


@gql.type
class Query:
    facsimile: Optional[Facsimile] = gql.django.node()
    facsimiles:  relay.Connection[Facsimile] = gql.django.connection()


@gql.type
class Mutation:
    create_facsimile: Facsimile = gql.django.create_mutation(FacsimileInput)
    update_facsimile: Facsimile = gql.django.update_mutation(FacsimilePartial)
    delete_facsimile: Facsimile = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, mutation=Mutation,
                    extensions=[DjangoOptimizerExtension])
