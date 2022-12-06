from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from mpcd.corpus.types.section_type import SectionType, SectionTypeInput, SectionTypePartial

from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (
    HasObjPerm,
    HasPerm,
    IsAuthenticated,
    IsStaff,
    IsSuperuser,
)


@gql.type
class Query:
    section_type: Optional[SectionType] = gql.django.node(directives=[IsAuthenticated()])
    section_types:  relay.Connection[SectionType] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:
    create_section_type: SectionType = gql.django.create_mutation(SectionTypeInput, directives=[IsAuthenticated()])
    update_section_type: SectionType = gql.django.update_mutation(SectionTypePartial, directives=[IsAuthenticated()])
    delete_section_type: SectionType = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
