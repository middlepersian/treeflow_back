from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.sentence import Sentence


@gql.type
class Query:
    sentence: Optional[Sentence] = gql.django.node()
    sentences:  relay.Connection[Sentence] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
