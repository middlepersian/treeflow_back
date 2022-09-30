from typing import List, TYPE_CHECKING
from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from strawberry.lazy_type import LazyType
from strawberry.dataloader import DataLoader
from asgiref.sync import sync_to_async
from collections import defaultdict
from django.contrib.auth import get_user_model

from mpcd.corpus.types.user import User

'''
UserModel = get_user_model()

async def batch_load_user(keys):
    users: List[UserModel] = sync_to_async(list)(UserModel.objects.filter(id__in=keys))

    user_dict = defaultdict()
    for user in users:
        if user.user_id not in user_dict:
            user_dict[user.user_id] = [user]
        else:
            user_dict[user.user_id].append(user)

    return [user_dict[key] for key in keys]

async def load_users(keys: List[int]) -> List[LazyType['User', 'mpcd.corpus.types.user']]:
    return [LazyType['User', 'mpcd.corpus.types.user'](id=key) for key in keys]

loader = DataLoader(load_fn=batch_load_user)

@gql.field
async def get_user(self, id: gql.ID) -> User:
    return await loader.load(id)

'''


@gql.type
class Query:
    users:  List[User] = gql.django.field()




schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
