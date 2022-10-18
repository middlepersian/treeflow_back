from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.dict.types.meaning import Meaning


@gql.type
class Query:
    meaning: Optional[Meaning] = gql.django.node()
    meanings:  relay.Connection[Meaning] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
