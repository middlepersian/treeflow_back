from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional, List
from django.core.exceptions import ValidationError

from mpcd.corpus.types.section import Section, SectionInput, SectionPartial


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
    section: Optional[Section] = gql.django.node(directives=[IsAuthenticated()])
    sections:  relay.Connection[Section] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:
    create_section: Section = gql.django.create_mutation(SectionInput, directives=[IsAuthenticated()])
    update_section: Section = gql.django.update_mutation(SectionPartial, directives=[IsAuthenticated()])
    delete_section: Section = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])

    @gql.django.mutation
    def set_previous_section(self, info, current_section: relay.GlobalID, previous_section: relay.GlobalID) -> Section:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        current = current_section.resolve_node(info)
        previous = previous_section.resolve_node(info)
        current.previous = previous
        current.save()
        return current

    @gql.django.mutation
    def add_tokens_to_section(self, info, section: relay.GlobalID, tokens: List[relay.GlobalID]) -> Section:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        section = section.resolve_node(info)
        tokens = [token.resolve_node(info) for token in tokens]
        section.tokens.set(tokens)
        section.save()
        return section


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
