from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import Annotated, TYPE_CHECKING

from mpcd.corpus import models

if TYPE_CHECKING:
    from .section import Section


@gql.django.type(models.SectionType)
class SectionType(relay.Node):
    section_section_type: relay.Connection[gql.LazyType['Section', 'mpcd.corpus.types.section']]

    id: gql.auto
    identifier: gql.auto


@gql.django.input(models.SectionType)
class SectionTypeInput:
    identifier: gql.auto


@gql.django.partial(models.SectionType)
class SectionTypePartial(gql.NodeInputPartial):
    id: gql.auto
    identifier: gql.auto
