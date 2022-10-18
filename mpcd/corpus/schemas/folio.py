import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from mpcd.corpus.types.folio import Folio, FolioInput, FolioPartial


@gql.type
class Query:
    folio: Optional[Folio] = gql.django.node()
    folios:  relay.Connection[Folio] = gql.django.connection()


@gql.type
class Mutation:
    create_folio: Folio = gql.django.create_mutation(FolioInput)
    update_folio: Folio = gql.django.update_mutation(FolioPartial)
    delete_folio: Folio = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, mutation=Mutation,extensions=[DjangoOptimizerExtension])
