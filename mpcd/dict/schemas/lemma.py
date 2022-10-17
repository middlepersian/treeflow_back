import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from mpcd.dict.types.lemma import Lemma


@gql.type
class Query:
    lemmas:  relay.Connection[Lemma] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
