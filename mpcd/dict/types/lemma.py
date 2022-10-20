
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from strawberry.lazy_type import LazyType
from typing import List, TYPE_CHECKING
from mpcd.dict import models


@gql.django.type(models.Lemma)
class Lemma(relay.Node):

    token_lemmas:  relay.Connection[LazyType['Token', 'mpcd.corpus.types.token']]

    id: gql.auto
    word: gql.auto
    language: gql.auto
    related_lemmas: List['Lemma']
    related_meanings: List[LazyType['Meaning', 'mpcd.dict.types.meaning']]
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]


@gql.django.input(models.Lemma)
class LemmaInput:
    word: gql.auto
    language: gql.auto
    related_lemmas: List['LemmaInput']
    related_meanings: List[LazyType['MeaningInput', 'mpcd.dict.types.meaning']]


@gql.django.partial(models.Lemma)
class LemmaPartial:
    id: gql.auto
    word: gql.auto
    language: gql.auto
    related_lemmas: List['LemmaPartial']
    related_meanings: List[LazyType['MeaningPartial', 'mpcd.dict.types.meaning']]
