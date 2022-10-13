import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from mpcd.corpus.types.user import User


@gql.type
class Query:
    users:  relay.Connection[User] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
