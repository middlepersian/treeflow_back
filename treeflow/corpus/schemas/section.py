import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional, List
from asgiref.sync import sync_to_async
from strawberry_django_plus.mutations import resolvers

from treeflow.corpus.types.section import Section, SectionInput, SectionPartial
from treeflow.corpus.models.section import Section as SectionModel

from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (

    IsAuthenticated,

)


@gql.type
class Query:
    section: Optional[Section] = gql.django.node()
    sections:  relay.Connection[Section] = gql.django.connection()

    @gql.field
    @sync_to_async
    def get_types(self) -> List[str]:
        section_types = SectionModel.objects.order_by('type').distinct('type').values_list('type', flat=True)
        return list(section_types)


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
    def create_section_between(self, info, previous_section: relay.GlobalID, new_section_data: SectionInput) -> Section:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        data = vars(new_section_data)
        previous = previous_section.resolve_node(info)
        new_section = resolvers.create(info, SectionModel, resolvers.parse_input(info, data))
        next_section = previous.next
        previous.next = new_section
        previous.save()
        if next_section:
            next_section.previous = new_section
            next_section.save()
        new_section.previous = previous
        new_section.next = next_section
        new_section.save()
        return new_section

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
