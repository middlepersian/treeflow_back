
from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Annotated
from mpcd.dict import models

if TYPE_CHECKING:
    from mpcd.corpus.types.token import Token
    from mpcd.corpus.types.comment import Comment
    from .meaning import Meaning


@gql.django.type(models.Lemma)
class Lemma(relay.Node):

    token_lemmas:  relay.Connection[Annotated['Token', lazy('mpcd.corpus.types.token')]]

    #id: gql.auto
    word: gql.auto
    language: gql.auto
    related_lemmas: List['Lemma']
    related_meanings: List[Annotated['Meaning', lazy('mpcd.dict.types.meaning')]]
    comments: List[Annotated['Comment', lazy('mpcd.corpus.types.comment')]]


@gql.django.input(models.Lemma)
class LemmaInput:
    word: gql.auto
    language: gql.auto
    related_lemmas: gql.auto
    related_meanings: gql.auto


@gql.django.partial(models.Lemma)
class LemmaPartial:
    id: gql.auto
    word: gql.auto
    language: gql.auto
    related_lemmas: gql.auto
    related_meanings: gql.auto
