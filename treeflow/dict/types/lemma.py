
import strawberry
from enum import Enum
from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List
from treeflow.dict import models
from treeflow.dict.types.language import Language
from django.db.models import Prefetch


@gql.django.filters.filter(models.Lemma, lookups=True)
class LemmaFilter:
    id: relay.GlobalID
    word: gql.auto
    language: Language
    multiword_expression: gql.auto


@gql.django.type(models.Lemma, filters=LemmaFilter)
class Lemma(relay.Node):

    token_lemmas:  relay.Connection[gql.LazyType['Token', 'treeflow.corpus.types.token']]
    comment_lemma: relay.Connection[gql.LazyType['Comment', 'treeflow.corpus.types.comment']]

    id: relay.GlobalID
    word: gql.auto
    language: Language
    multiword_expression: gql.auto
    related_lemmas: List['Lemma']
    related_meanings: List[gql.LazyType['Meaning', 'treeflow.dict.types.meaning']]



@gql.django.input(models.Lemma)
class LemmaInput:
    word: gql.auto
    language: Language
    multiword_expression: gql.auto
    related_lemmas: gql.auto
    related_meanings: gql.auto


@gql.django.partial(models.Lemma)
class LemmaPartial:
    id: relay.GlobalID
    word: gql.auto
    language: Language
    multiword_expression: gql.auto
    related_lemmas: gql.auto
    related_meanings: gql.auto
