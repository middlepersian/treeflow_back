from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import Annotated, TYPE_CHECKING

from treeflow.corpus import models

if TYPE_CHECKING:
    from .section import Section


@gql.django.type(models.SectionType)
class SectionType(relay.Node):
    section_section_type: relay.Connection[gql.LazyType['Section', 'treeflow.corpus.types.section']]

    id: relay.GlobalID
    identifier: gql.auto


@gql.django.input(models.SectionType)
class SectionTypeInput:
    identifier: gql.auto


@gql.django.partial(models.SectionType)
class SectionTypePartial(gql.NodeInputPartial):
    id: relay.GlobalID
    identifier: gql.auto
