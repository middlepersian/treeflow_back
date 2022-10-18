from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional
from strawberry.lazy_type import LazyType

from mpcd.corpus import models



@gql.django.type(models.Section)
class Section(relay.Node):
    id: gql.auto
    number: gql.auto
    identifier: gql.auto
    text: Optional[LazyType['Text', 'mpcd.corpus.types.text']]
    section_type:  Optional[LazyType['SectionType', 'mpcd.corpus.types.section_type']]
    source:  Optional[LazyType['Source', 'mpcd.corpus.types.source']]
    tokens: List[LazyType['Token', 'mpcd.corpus.types.token']]
    previous: Optional['Section']
    container: Optional['Section']
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]
