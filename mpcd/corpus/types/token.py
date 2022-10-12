
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional
from strawberry.lazy_type import LazyType

from mpcd.corpus import models

if TYPE_CHECKING:
    from mpcd.corpus.types.dependency import Dependency
    from mpcd.corpus.types.text import Text
    from mpcd.corpus.types.token_comment import TokenComment
    from mpcd.corpus.types.line import Line
    from mpcd.corpus.types.morphological_annotation import MorphologicalAnnotation
    from mpcd.dict.types.lemma import Lemma
    from mpcd.dict.types.meaning import Meaning


@gql.django.type(models.Token)
class Token(relay.Node):
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
