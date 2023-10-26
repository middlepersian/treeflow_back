import strawberry
import strawberry_django
from strawberry import relay
from typing import List, Optional, Iterable
from treeflow.dict import models
from strawberry.types import Info
from asgiref.sync import sync_to_async
from treeflow.dict.enums.language import Language


@strawberry_django.filters.filter(models.Meaning, lookups=True)
class MeaningFilter:
    id: Optional[relay.GlobalID]
    meaning: strawberry.auto
    language: Optional[Language]
    lemma_related: strawberry.auto


@strawberry_django.type(models.Meaning, filters=Optional[MeaningFilter])
class Meaning(relay.Node):

    token_meanings:  List[strawberry.LazyType['Token',
                                              'treeflow.corpus.types.token']] = strawberry_django.field()
    sentence_meanings:  List[strawberry.LazyType['Meaning',
                                                 'treeflow.dict.types.meaning']] = strawberry_django.field()
    comment_meaning: List[strawberry.LazyType['Comment',
                                              'treeflow.corpus.types.comment']] = strawberry_django.field()

    id: relay.NodeID[str]
    meaning: strawberry.auto
    language: Language
    related_meanings: List['Meaning']
    related_lemmas: List[strawberry.LazyType['Lemma',
                                             'treeflow.dict.types.lemma']]


@strawberry_django.input(models.Meaning)
class MeaningInput:
    meaning: strawberry.auto
    language: Language
    related_meanings: Optional[List['Meaning']]


@strawberry_django.partial(models.Meaning)
class MeaningPartial:
    id: relay.GlobalID
    meaning: strawberry.auto
    language: Optional[Language]
    related_meanings: strawberry.auto


# create input type for search
@strawberry.input
class MeaningSelectionInput:
    meaning: Optional[str]
    language: Optional[Language]
