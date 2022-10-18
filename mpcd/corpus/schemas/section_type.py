from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.section_type import SectionType


@gql.type
class Query:
    section_type: Optional[SectionType] = gql.django.node()
    section_types:  relay.Connection[SectionType] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
