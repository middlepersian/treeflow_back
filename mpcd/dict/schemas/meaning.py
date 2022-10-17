import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from mpcd.dict.types.meaning import Meaning


@gql.type
class Query:
    meanings:  relay.Connection[Meaning] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
