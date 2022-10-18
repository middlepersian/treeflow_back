from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from mpcd.corpus.types.facsimile import Facsimile


@gql.type
class Query:
    facsimile: Optional[Facsimile] = gql.django.node()
    facsimiles:  relay.Connection[Facsimile] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
