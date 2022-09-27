from typing import List
from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from strawberry.lazy_type import LazyType
from mpcd.corpus.types.comment import Comment


@gql.type
class Query:
    comments:  List[LazyType['Comment', 'mpcd.corpus.types.comment']] = gql.django.field()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
