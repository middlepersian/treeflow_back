from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.section import Section, SectionInput, SectionPartial


@gql.type
class Query:
    section: Optional[Section] = gql.django.node()
    sections:  relay.Connection[Section] = gql.django.connection()


@gql.type
class Mutation:
    create_section: Section = gql.django.create_mutation(SectionInput)
    update_section: Section = gql.django.update_mutation(SectionPartial)
    delete_section: Section = gql.django.delete_mutation(gql.NodeInput)


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
