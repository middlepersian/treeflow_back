from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional

from mpcd.corpus import models


if TYPE_CHECKING:
    from mpcd.dict.types.lemma import Lemma
    from mpcd.dict.types.meaning import Meaning
    from .comment import Comment
    from .dependency import Dependency
    from .line import Line
    from .morphological_annotation import MorphologicalAnnotation
    from .section import Section
    from .text import Text
    from .sentence import Sentence

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

    section_tokens: List[gql.LazyType['Section', 'mpcd.corpus.types.section']]
    comment_token: List[gql.LazyType['Comment', 'mpcd.corpus.types.comment']]

    id: relay.GlobalID
    number: gql.auto
    text: gql.LazyType['Text', 'mpcd.corpus.types.text']
    sentence: gql.LazyType['Sentence', 'mpcd.corpus.types.sentence']
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: List[gql.LazyType['Lemma', 'mpcd.dict.types.lemma']]
    meanings: List[gql.LazyType['Meaning', 'mpcd.dict.types.meaning']]
    pos: gql.auto
    morphological_annotation: List[gql.LazyType['MorphologicalAnnotation',
                                                'mpcd.corpus.types.morphological_annotation']]
    syntactic_annotation: List[gql.LazyType['Dependency', 'mpcd.corpus.types.dependency']]
    avestan: gql.auto
    line: gql.LazyType['Line', 'mpcd.corpus.types.line']
    previous: Optional['Token']
    next: Optional['Token']
    gloss: gql.auto


@gql.django.input(models.Token)
class TokenInput:
    number: gql.auto
    text: gql.auto
    sentence: gql.auto
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: gql.auto
    meanings: gql.auto
    pos: gql.auto
    morphological_annotation: gql.auto
    syntactic_annotation: gql.auto
    avestan: gql.auto
    line: gql.auto
    previous: gql.auto
    next: gql.auto
    gloss: gql.auto


@gql.django.partial(models.Token)
class TokenPartial:
    id: relay.GlobalID
    number: gql.auto
    text: gql.auto
    sentence: gql.auto
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: gql.auto
    meanings: gql.auto
    pos: gql.auto
    morphological_annotation: gql.auto
    syntactic_annotation: gql.auto
    avestan: gql.auto
    line: gql.auto
    previous: gql.auto
    next: gql.auto
    gloss: gql.auto
