from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional
from strawberry.lazy_type import LazyType

from mpcd.corpus import models


@gql.django.type(models.Sentence)
class Sentence(relay.Node):
    id: gql.auto
    number: float
    text: LazyType['Text', 'mpcd.corpus.types.text']
    tokens: List[LazyType['Token', 'mpcd.corpus.types.token']]
    translations: List[LazyType['Meaning', 'mpcd.dict.types.meaning']]
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]
    previous: Optional[LazyType['Sentence', 'mpcd.corpus.types.sentence']]


@gql.django.input(models.Sentence)
class SentenceInput:
    number: float
    text: gql.auto
    # see how this works
    tokens: gql.auto
    translations: Optional[List[LazyType['MeaningInput', 'mpcd.dict.types.meaning']]]
    comments: Optional[List[LazyType['CommentInput', 'mpcd.corpus.types.comment']]]
    previous: gql.auto


@gql.django.partial(models.Sentence)
class SentencePartial:
    id: gql.auto
    number: float
    text: gql.auto
    # see how this works
    tokens: gql.auto
    translations: Optional[List[LazyType['MeaningPartial', 'mpcd.dict.types.meaning']]]
    comments: Optional[List[LazyType['CommentPartial', 'mpcd.corpus.types.comment']]]
    previous: gql.auto
