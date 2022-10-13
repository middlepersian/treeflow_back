from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional
from strawberry.lazy_type import LazyType

from mpcd.corpus import models


if TYPE_CHECKING:
    from mpcd.corpus.types.text import Text
    from mpcd.corpus.types.token import Token
    from mpcd.corpus.types.comment import Comment
    from mpcd.dict.types.meaning import Meaning


@gql.django.type(models.Sentence)
class Sentence(relay.Node):
    id: gql.auto
    number: float
    text: LazyType['Text', 'mpcd.corpus.types.text']
    tokens: List[LazyType['Token', 'mpcd.corpus.types.token']]
    translations: List[LazyType['Meaning', 'mpcd.dict.types.meaning']]
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]
    previous: Optional[LazyType['Sentence', 'mpcd.corpus.types.sentence']]
