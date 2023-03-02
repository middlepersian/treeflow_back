
import strawberry
from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import Annotated, List, TYPE_CHECKING
from treeflow.dict import models
from treeflow.dict.types import language

if TYPE_CHECKING:
    from treeflow.corpus.types.token import Token
    from treeflow.corpus.types.comment import Comment
    from treeflow.dict.types.meaning import Meaning


@gql.django.filters.filter(models.Meaning, lookups=True)
class MeaningFilter:
    id: relay.GlobalID
    meaning: gql.auto
    language: gql.auto


@gql.django.type(models.Meaning, filters=MeaningFilter)
class Meaning(relay.Node):

    token_meanings:  relay.Connection[gql.LazyType['Token', 'treeflow.corpus.types.token']]
    sentence_meanings:  relay.Connection[gql.LazyType['Meaning', 'treeflow.dict.types.meaning']]
    comment_meaning: relay.Connection[gql.LazyType['Comment', 'treeflow.corpus.types.comment']]

    id: relay.GlobalID
    meaning: gql.auto
    language: gql.auto
    related_meanings: List['Meaning']


@gql.django.input(models.Meaning)
class MeaningInput:
    meaning: gql.auto
    language: gql.auto
    related_meanings: gql.auto


@gql.django.partial(models.Meaning)
class MeaningPartial:
    id: relay.GlobalID
    meaning: gql.auto
    language: gql.auto
    related_meanings: gql.auto



@strawberry.type
class MeaningElastic:
    id: relay.GlobalID
    meaning: str
    language: str
    related_meanings: List[str]    
