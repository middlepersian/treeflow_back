from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional

from treeflow.corpus import models


if TYPE_CHECKING:
    from treeflow.dict.types.lemma import Lemma
    from treeflow.dict.types.meaning import Meaning
    from .comment import Comment
    from .dependency import Dependency
    from .morphological_annotation import MorphologicalAnnotation
    from .section import Section
    from .text import Text


@gql.django.filters.filter(models.Text)
class TextFilter:
    id: relay.GlobalID
    title: gql.auto


@gql.django.filters.filter(models.Token, lookups=True)
class TokenFilter:
    id: relay.GlobalID
    transcription: gql.auto
    transliteration: gql.auto
    language: gql.auto
    number: gql.auto
    text: 'TextFilter'


@gql.django.type(models.Token, filters=TokenFilter)
class Token(relay.Node):

    section_tokens: List[gql.LazyType['Section', 'treeflow.corpus.types.section']]
    comment_token: List[gql.LazyType['Comment', 'treeflow.corpus.types.comment']]

    id: relay.GlobalID
    number: gql.auto
    text: gql.LazyType['Text', 'treeflow.corpus.types.text']
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: List[gql.LazyType['Lemma', 'treeflow.dict.types.lemma']]
    meanings: List[gql.LazyType['Meaning', 'treeflow.dict.types.meaning']]
    pos: gql.auto
    morphological_annotation: List[gql.LazyType['MorphologicalAnnotation',
                                                'treeflow.corpus.types.morphological_annotation']]
    syntactic_annotations: List[gql.LazyType['Dependency', 'treeflow.corpus.types.dependency']]
    avestan: gql.auto
    previous: Optional['Token']
    next: Optional['Token']
    gloss: gql.auto


@gql.django.input(models.Token)
class TokenInput:
    number: gql.auto
    text: gql.auto
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: gql.auto
    meanings: gql.auto
    pos: gql.auto
    morphological_annotations: gql.auto
    syntactic_annotations: gql.auto
    avestan: gql.auto
    previous: gql.auto
    next: gql.auto
    gloss: gql.auto


@gql.django.partial(models.Token)
class TokenPartial:
    id: relay.GlobalID
    number: gql.auto
    text: gql.auto
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: gql.auto
    meanings: gql.auto
    pos: gql.auto
    morphological_annotations: gql.auto
    syntactic_annotations: gql.auto
    avestan: gql.auto
    previous: gql.auto
    next: gql.auto
    gloss: gql.auto
