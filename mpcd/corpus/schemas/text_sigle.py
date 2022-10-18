from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from mpcd.corpus.types.text_sigle import TextSigle


@gql.type
class Query:
    text_sigle: Optional[TextSigle] = gql.django.node()
    text_sigles:  relay.Connection[TextSigle] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
