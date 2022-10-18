
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional
from strawberry.lazy_type import LazyType

from mpcd.corpus import models


@gql.django.type(models.Token)
class Token(relay.Node):

    section_tokens: List[LazyType['Section', 'mpcd.corpus.types.section']]

    id: gql.auto
    number: gql.auto
    text: LazyType['Text', 'mpcd.corpus.types.text']
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: List[LazyType['Lemma', 'mpcd.dict.types.lemma']]
    meanings: List[LazyType['Meaning', 'mpcd.dict.types.meaning']]
    pos: gql.auto
    morphological_annotation: List[LazyType['MorphologicalAnnotation', 'mpcd.corpus.types.morphological_annotation']]
    syntactic_annotation: List[LazyType['Dependency', 'mpcd.corpus.types.dependency']]
    comments: List[LazyType['TokenComment', 'mpcd.corpus.types.token_comment']]
    avestan: gql.auto
    line: LazyType['Line', 'mpcd.corpus.types.line']
    previous: Optional['Token']
    gloss: gql.auto


@gql.django.type(models.Token)
class TokenInput:
    id: gql.auto
    number: gql.auto
    text: gql.auto
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: Optional[List[gql.NodeInput]]
    meanings: Optional[List[gql.NodeInput]]
    pos: gql.auto
    morphological_annotation: Optional[List[gql.NodeInput]]
    syntactic_annotation: Optional[List[gql.NodeInput]]
    comments: Optional[List[gql.NodeInput]]
    avestan: gql.auto
    line: gql.auto
    previous: Optional['Token']
    gloss: gql.auto
