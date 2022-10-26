
from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import Annotated, List, TYPE_CHECKING
from mpcd.dict import models

if TYPE_CHECKING:
    from mpcd.corpus.types.token import Token
    from mpcd.corpus.types.comment import Comment


@gql.django.type(models.Meaning)
class Meaning(relay.Node):

    token_meanings:  relay.Connection[Annotated['Token', lazy('mpcd.corpus.types.token')]]

    id: gql.auto
    meaning: gql.auto
    language: gql.auto
    related_meanings: List['Meaning']
    comments: List[Annotated['Comment', lazy('mpcd.corpus.types.comment')]]


@gql.django.input(models.Meaning)
class MeaningInput:
    meaning: gql.auto
    language: gql.auto
    related_meanings: gql.auto
    comments: gql.auto


@gql.django.partial(models.Meaning)
class MeaningPartial:
    id: gql.auto
    meaning: gql.auto
    language: gql.auto
    related_meanings: gql.auto
    comments: gql.auto
