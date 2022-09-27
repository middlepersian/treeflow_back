from typing import List
from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from mpcd.corpus.types.token import Token
@gql.type
class Query:
    tokens: List[Token] = gql.django.field()



schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
