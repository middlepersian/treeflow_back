
from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Annotated
from mpcd.dict import models
from mpcd.dict.types import language

if TYPE_CHECKING:
    from mpcd.corpus.types.token import Token
    from mpcd.corpus.types.comment import Comment
    from .meaning import Meaning


@gql.django.filters.filter(models.Lemma, lookups=True)
class LemmaFilter:
    id: relay.GlobalID
    word: gql.auto
    language : gql.auto


@gql.django.type(models.Lemma, filters=LemmaFilter)
class Lemma(relay.Node):

    token_lemmas:  relay.Connection[gql.LazyType['Token', 'mpcd.corpus.types.token']]

    id: relay.GlobalID
    word: gql.auto
    language : gql.auto
    related_lemmas: List['Lemma']
    related_meanings: List[gql.LazyType['Meaning', 'mpcd.dict.types.meaning']]
    comments: List[gql.LazyType['Comment', 'mpcd.corpus.types.comment']]



@gql.django.input(models.Lemma)
class LemmaInput:
    word: gql.auto
    language : gql.auto

    related_lemmas: gql.auto
    related_meanings: gql.auto


@gql.django.partial(models.Lemma)
class LemmaPartial:
    id: gql.auto
    word: gql.auto
    language : gql.auto

    related_lemmas: gql.auto
    related_meanings: gql.auto
