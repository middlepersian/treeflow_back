from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from django.core.exceptions import ValidationError

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

    @gql.django.input_mutation
    def set_previous_section(self, info, current_section_id: relay.GlobalID, previous_section_id: relay.GlobalID) -> Section:
        ## get the current section
        current_section = relay.from_global_id(current_section_id)
        obj = id.resolve_node(info)
        if obj.some_field == "some_value":
            raise ValidationError("Cannot update obj with some_value")

        return obj


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
