
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from strawberry.lazy_type import LazyType
from typing import List, TYPE_CHECKING
from mpcd.dict import models
if TYPE_CHECKING:
    from mpcd.dict.types import Meaning
    from mpcd.corpus.types.comment import Comment


@gql.django.type(models.Lemma)
class Lemma:
    id: gql.auto
    word: gql.auto
    language: gql.auto
    related_lemmas: List['Lemma']
    related_meanings: List[LazyType['Meaning', 'mpcd.dict.types.meaning']]
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]
