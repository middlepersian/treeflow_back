from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from mpcd.corpus.types.corpus import Corpus


@gql.type
class Query:
    corpus: Optional[Corpus] = gql.django.node()
    corpora:  relay.Connection[Corpus] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
