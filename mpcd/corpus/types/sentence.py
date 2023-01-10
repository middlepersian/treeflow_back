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

    token_sentence: List[gql.LazyType['Token', 'mpcd.corpus.types.token']]
    comment_sentence: List[gql.LazyType['Comment', 'mpcd.corpus.types.comment']]

    id: relay.GlobalID
    number: float
    text: gql.LazyType['Text', 'mpcd.corpus.types.text']
    meanings: List[gql.LazyType['Meaning', 'mpcd.dict.types.meaning']]
    previous: Optional[gql.LazyType['Sentence', 'mpcd.corpus.types.sentence']]
    next: Optional[gql.LazyType['Sentence', 'mpcd.corpus.types.sentence']]


@gql.django.input(models.Sentence)
class SentenceInput:
    number: float
    text: gql.auto
    meanings: gql.auto
    previous: gql.auto
    next: gql.auto


@gql.django.partial(models.Sentence)
class SentencePartial:
    id: relay.GlobalID
    number: float
    text: gql.auto
    meanings: gql.auto
    previous: gql.auto
    next: gql.auto
