from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from mpcd.corpus.types.dependency import Dependency


@gql.type
class Query:
    dependency: Optional[Dependency] = gql.django.node()
    dependencies:  relay.Connection[Dependency] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
