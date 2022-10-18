from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.section_type import SectionType, SectionTypeInput, SectionTypePartial


@gql.type
class Query:
    section_type: Optional[SectionType] = gql.django.node()
    section_types:  relay.Connection[SectionType] = gql.django.connection()


@gql.type
class Mutation:
    create_section_type: SectionType = gql.django.create_mutation(SectionTypeInput)
    update_section_type: SectionType = gql.django.update_mutation(SectionTypePartial)
    delete_section_type: SectionType = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
