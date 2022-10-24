from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional, Annotated

from mpcd.corpus import models

if TYPE_CHECKING:
    from mpcd.dict.types.lemma import Lemma
    from mpcd.dict.types.meaning import Meaning
    from. dependency import Dependency
    from .line import Line
    from .morphological_annotation import MorphologicalAnnotation
    from .section import Section
    from .text import Text
    from .token_comment import TokenComment


@gql.django.type(models.Token)
class Token(relay.Node):

    section_tokens: List[Annotated['Section', lazy('mpcd.corpus.types.section')]]

    id: gql.auto
    number: gql.auto
    text: Annotated['Text', lazy('mpcd.corpus.types.text')]
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: List[Annotated['Lemma', lazy('mpcd.dict.types.lemma')]]
    meanings: List[Annotated['Meaning', lazy('mpcd.dict.types.meaning')]]
    pos: gql.auto
    morphological_annotation: List[Annotated['MorphologicalAnnotation',
                                             lazy('mpcd.corpus.types.morphological_annotation')]]
    syntactic_annotation: List[Annotated['Dependency', lazy('mpcd.corpus.types.dependency')]]
    comments: List[Annotated['TokenComment', lazy('mpcd.corpus.types.token_comment')]]
    avestan: gql.auto
    line: Annotated['Line', lazy('mpcd.corpus.types.line')]
    previous: Optional['Token']
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
    morphological_annotation: gql.auto
    syntactic_annotation: gql.auto
    comments: gql.auto
    avestan: gql.auto
    line: gql.auto
    previous: gql.auto
    gloss: gql.auto


@gql.django.partial(models.Token)
class TokenPartial:
    id: gql.auto
    number: gql.auto
    text: gql.auto
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: gql.auto
    meanings: gql.auto
    pos: gql.auto
    morphological_annotation: gql.auto
    syntactic_annotation: gql.auto
    comments: gql.auto
    avestan: gql.auto
    line: gql.auto
    previous: gql.auto
    gloss: gql.auto
