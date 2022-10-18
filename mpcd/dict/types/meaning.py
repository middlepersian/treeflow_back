
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from strawberry.lazy_type import LazyType
from typing import List, TYPE_CHECKING
from mpcd.dict import models


@gql.django.type(models.Meaning)
class Meaning(relay.Node):
    
    token_meanings:  relay.Connection[LazyType['Token', 'mpcd.corpus.types.token']]

    id: gql.auto
    meaning: gql.auto
    language: gql.auto
    related_meanings: List['Meaning']
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]
