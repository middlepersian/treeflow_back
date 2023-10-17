import strawberry
import strawberry_django
from strawberry import relay
from typing import List, Optional, Iterable
from treeflow.dict import models
from treeflow.dict.enums.term_tech import TermTech
from treeflow.dict.enums.language import Language
from strawberry.types import Info
from elasticsearch.exceptions import NotFoundError
from asgiref.sync import sync_to_async


@strawberry.type
class TermTechList:
    term_tech: List[TermTech]


@strawberry.type
class LanguageList:
    language: List[Language]


@strawberry_django.filters.filter(models.Lemma, lookups=True)
class LemmaFilter:
    id: Optional[relay.GlobalID]
    word: strawberry.auto
    language: Optional[Language]
    multiword_expression: strawberry.auto


@strawberry_django.type(models.Lemma, filters=Optional[LemmaFilter])
class Lemma(relay.Node):

    token_lemmas:  List[strawberry.LazyType['Token',
                                            'treeflow.corpus.types.token']] = strawberry_django.field()
    comment_lemma: List[strawberry.LazyType['Comment',
                                            'treeflow.corpus.types.comment']] = strawberry_django.field()

    id: relay.NodeID[str]
    word: strawberry.auto
    language: Language
    multiword_expression: strawberry.auto
    categories: Optional[List[Optional[str]]]
    related_lemmas: List['Lemma']
    related_meanings: List[strawberry.LazyType['Meaning',
                                               'treeflow.dict.types.meaning']]


@strawberry_django.input(models.Lemma)
class LemmaInput:
    word: strawberry.auto
    language: Language
    multiword_expression: strawberry.auto
    categories: Optional[List[Optional[str]]]
    related_lemmas: strawberry.auto
    related_meanings: strawberry.auto


@strawberry_django.partial(models.Lemma)
class LemmaPartial:
    id: relay.GlobalID
    word: strawberry.auto
    language: Optional[Language]
    multiword_expression: strawberry.auto
    categories: Optional[List[Optional[str]]]
    related_lemmas: strawberry.auto
    related_meanings: strawberry.auto


