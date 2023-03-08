from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, Optional, cast
from django.db.models import Prefetch
from strawberry.types.info import Info

from treeflow.corpus import models
#from .token import TextFilter
#from treeflow.images.types.image import ImageFilter




@gql.django.filters.filter(models.Section)
class SectionFilter:
    id: relay.GlobalID
    type: gql.auto
    container: 'SectionFilter'
    text:  gql.LazyType['TextFilter', 'treeflow.corpus.types.text']
    image : gql.LazyType['ImageFilter', 'treeflow.images.types.image']


@gql.django.type(models.Section, filters=SectionFilter)
class Section(relay.Node):
    comment_section: List[gql.LazyType['Comment', 'treeflow.corpus.types.comment']]

    id: relay.GlobalID
    number: gql.auto
    identifier: gql.auto
    title: gql.auto
    type: gql.auto
    text: Optional[gql.LazyType['Text', 'treeflow.corpus.types.text']]
    source:  Optional[gql.LazyType['Source', 'treeflow.corpus.types.source']]
    tokens: List[gql.LazyType['Token', 'treeflow.corpus.types.token']]
    meanings: List[gql.LazyType['Meaning', 'treeflow.dict.types.meaning']]
    previous: Optional['Section']
    next: Optional['Section']
    container: Optional['Section']

    @gql.django.field(
        prefetch_related=[
            "section_container"
        ],
    )
    def contains_sections(self, info: Info) -> List[gql.LazyType['Section', 'treeflow.corpus.types.section']]:
        return [cast(Section, section) for section in self.section_container.all()]
    
    
    @gql.django.field(
        prefetch_related=[
            "tokens"
        ],
    )
    def resolve_tokens(self, info: Info) -> List[gql.LazyType['Token', 'treeflow.corpus.types.token']]:
        return [gql.LazyType('Token', token.pk) for token in self.tokens.all()]


    @gql.django.field(
        prefetch_related=[
            "meanings"
        ],
    )
    def resolve_meanings(self, info: Info) -> List[gql.LazyType['Meaning', 'treeflow.dict.types.meaning']]:
        return [gql.LazyType('Meaning', meaning.pk) for meaning in self.meanings.all()]     
    
@gql.django.input(models.Section)
class SectionInput:
    number: gql.auto
    identifier: gql.auto
    title: gql.auto
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
    title: gql.auto
    identifier: gql.auto
    text: gql.auto
    type: gql.auto
    source: gql.auto
    tokens: gql.auto
    previous: gql.auto
    meanings: gql.auto
    next: gql.auto
    container: gql.auto
