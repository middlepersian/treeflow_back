from typing import List
from collections import defaultdict
from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from strawberry.lazy_type import LazyType
from strawberry.dataloader import DataLoader

from mpcd.corpus.types.comment import Comment


async def load_comments(keys: List[int]) -> List[LazyType['Comment', 'mpcd.corpus.types.comment']]:
    return [LazyType['Comment', 'mpcd.corpus.types.comment'](id=key) for key in keys]


loader = DataLoader(load_fn=load_comments)


@gql.type
class Query:
    comments:  List[Comment] = gql.django.field()

    @gql.field
    async def get_comment(self, id: gql.ID) -> Comment:
        return await loader.load(id)


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
