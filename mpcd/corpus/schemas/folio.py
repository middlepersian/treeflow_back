import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from mpcd.corpus.types.folio import Folio


@gql.type
class Query:
    folio: Optional[Folio] = gql.django.node()
    folios:  relay.Connection[Folio] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
