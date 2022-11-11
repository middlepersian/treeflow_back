from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional, Annotated

from mpcd.corpus import models

if TYPE_CHECKING:
    from .comment import Comment
    from .text import Text
    from .section_type import SectionType
    from .source import Source
    from .token import Token


@gql.django.type(models.Section)
class Section(relay.Node):
    #id: gql.auto
    number: gql.auto
    identifier: gql.auto
    text: Optional[gql.LazyType['Text', 'mpcd.corpus.types.text']]
    section_type:  Optional[gql.LazyType['SectionType', 'mpcd.corpus.types.section_type']]
    source:  Optional[gql.LazyType['Source', 'mpcd.corpus.types.source']]
    tokens: List[gql.LazyType['Token', 'mpcd.corpus.types.token']]
    previous: Optional['Section']
    container: Optional['Section']
    comments: List[gql.LazyType['Comment', 'mpcd.corpus.types.comment']]


@gql.django.input(models.Section)
class SectionInput:
    number: gql.auto
    identifier: gql.auto
    text: gql.auto
    section_type: gql.auto
    source: gql.auto
    tokens: gql.auto
    previous: gql.auto
    container: gql.auto
    comments:  gql.auto


@gql.django.partial(models.Section)
class SectionPartial:
    id: gql.auto
    number: gql.auto
    identifier: gql.auto
    text: gql.auto
    section_type: gql.auto
    source: gql.auto
    tokens: gql.auto
    previous: gql.auto
    container: gql.auto
    comments: gql.auto
