from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, Optional

from treeflow.corpus import models
from .token import TextFilter



@gql.django.filters.filter(models.Section)
class SectionFilter:
    id: relay.GlobalID
    type: gql.auto
    container: 'SectionFilter'
    text: 'TextFilter'


@gql.django.type(models.Section, filters=SectionFilter)
class Section(relay.Node):
    id: relay.GlobalID
    number: gql.auto
    identifier: gql.auto
    type: gql.auto
    text: Optional[gql.LazyType['Text', 'treeflow.corpus.types.text']]
    source:  Optional[gql.LazyType['Source', 'treeflow.corpus.types.source']]
    tokens: relay.Connection[gql.LazyType['Token', 'treeflow.corpus.types.token']]
    meanings: List[gql.LazyType['Meaning', 'treeflow.dict.types.meaning']]
    previous: Optional['Section']
    next: Optional['Section']
    container: Optional['Section']


@gql.django.input(models.Section)
class SectionInput:
    number: gql.auto
    identifier: gql.auto
    text: gql.auto
    type: gql.auto
    source: gql.auto
    tokens: gql.auto
    meanings: gql.auto
    previous: gql.auto
    next: gql.auto
    container: gql.auto


@gql.django.partial(models.Section)
class SectionPartial:
    id: relay.GlobalID
    number: gql.auto
    identifier: gql.auto
    text: gql.auto
    type: gql.auto
    source: gql.auto
    tokens: gql.auto
    previous: gql.auto
    meanings: gql.auto
    next: gql.auto
    container: gql.auto
