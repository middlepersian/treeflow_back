from typing import List
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from strawberry.lazy_type import LazyType
from mpcd.corpus.types.token_comment import TokenComment


@gql.type
class Query:
    token_comments:  relay.Connection[TokenComment] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
