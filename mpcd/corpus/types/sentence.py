from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional, Annotated

from mpcd.corpus import models

if TYPE_CHECKING:
    from .comment import Comment
    from mpcd.dict.types import Meaning
    from .sentence import Sentence
    from .text import Text
    from .token import Token


@gql.django.type(models.Sentence)
class Sentence(relay.Node):
    id: gql.auto
    number: float
    text: Annotated['Text', lazy('mpcd.corpus.types.text')]
    tokens: List[Annotated['Token', lazy('mpcd.corpus.types.token')]]
    translations: List[Annotated['Meaning', lazy('mpcd.dict.types.meaning')]]
    comments: List[Annotated['Comment', lazy('mpcd.corpus.types.comment')]]
    previous: Optional[Annotated['Sentence', lazy('mpcd.corpus.types.sentence')]]


@gql.django.input(models.Sentence)
class SentenceInput:
    number: float
    text: gql.auto
    tokens: gql.auto
    translations: gql.auto
    comments: gql.auto
    previous: gql.auto


@gql.django.partial(models.Sentence)
class SentencePartial:
    id: gql.auto
    number: float
    text: gql.auto
    tokens: gql.auto
    translations: gql.auto
    comments: gql.auto
    previous: gql.auto
