from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional, List
from asgiref.sync import sync_to_async

from treeflow.corpus.types.text import Text, TextInput, TextPartial
from treeflow.corpus.models.text import Text as TextModel
from treeflow.corpus.models.section import Section as SectionModel

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
    text: Optional[Text] = gql.django.node()
    texts: relay.Connection[Text] = gql.django.connection()

    @gql.field
    @sync_to_async
    def get_section_types_in_text(self, info, text_id: relay.GlobalID) -> List[str]:

        # Get the text object
        text = text_id.resolve_node(info)

        # Get all related sections
        sections = SectionModel.objects.filter(text=text)

        # Get all types
        section_types = sections.values_list('type', flat=True)

        # Make the section types unique by converting them to a set
        unique_section_types = list(set(section_types))

        return unique_section_types

@gql.type
class Mutation:
    create_text: Text = gql.django.create_mutation(TextInput, directives=[IsAuthenticated()])
    update_text: Text = gql.django.update_mutation(TextPartial, directives=[IsAuthenticated()])
    delete_text: Text = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation,  extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
