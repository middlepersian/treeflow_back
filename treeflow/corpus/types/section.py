from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional, Annotated

from treeflow.corpus import models
from .token import TextFilter
if TYPE_CHECKING:
    from .comment import Comment
    from .text import Text
    from .section_type import SectionType
    from .source import Source
    from .token import Token


@gql.django.filters.filter(models.SectionType)
class SectionTypeFilter:
    id: relay.GlobalID
    identifier: gql.auto


@gql.django.filters.filter(models.Section)
class SectionFilter:
    id: relay.GlobalID
    section_type: 'SectionTypeFilter'
    container: 'SectionFilter'
    section_container: 'SectionFilter'
    text: 'TextFilter'


@gql.django.type(models.Section, filters=SectionFilter)
class Section(relay.Node):
    id: relay.GlobalID
    number: gql.auto
    identifier: gql.auto
    text: Optional[gql.LazyType['Text', 'treeflow.corpus.types.text']]
    section_type:  Optional[gql.LazyType['SectionType', 'treeflow.corpus.types.section_type']]
    source:  Optional[gql.LazyType['Source', 'treeflow.corpus.types.source']]
    tokens: List[gql.LazyType['Token', 'treeflow.corpus.types.token']]
    previous: Optional['Section']
    next: Optional['Section']
    container: Optional['Section']
    section_container: Optional['Section']


@gql.django.input(models.Section)
class SectionInput:
    number: gql.auto
    identifier: gql.auto
    text: gql.auto
    section_type: gql.auto
    source: gql.auto
    tokens: gql.auto
    previous: gql.auto
    #next: gql.auto
    container: gql.auto


@gql.django.partial(models.Section)
class SectionPartial:
    id: relay.GlobalID
    number: gql.auto
    identifier: gql.auto
    text: gql.auto
    section_type: gql.auto
    source: gql.auto
    tokens: gql.auto
    previous: gql.auto
    #next: gql.auto
    container: gql.auto
