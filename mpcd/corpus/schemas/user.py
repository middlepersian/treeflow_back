import strawberry
from typing import List, TYPE_CHECKING
from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from strawberry.lazy_type import LazyType
from strawberry.dataloader import DataLoader
from asgiref.sync import sync_to_async
from collections import defaultdict
from django.contrib.auth import get_user_model
from django.db.models import Model as DjangoModel
from mpcd.corpus.types.user import User


UserModel = get_user_model()


@sync_to_async
def load_fn(keys: list[str]) -> list[User]:
    instances: list[User] = list(UserModel.objects.filter(pk__in=keys))
    # ensure instances are ordered in the same way as input 'keys'
    id_to_instance: dict[str, UserModel] = {inst.pk: inst for inst in instances}
    return [id_to_instance.get(id_) for id_ in keys]


async def load_users(keys: List[int]) -> List[LazyType['User', 'mpcd.corpus.types.user']]:
    return [LazyType['User', 'mpcd.corpus.types.user'](id=key) for key in keys]

loader = DataLoader(load_fn=load_users)


@gql.type
class Query:
    users:  List[User] = gql.django.field()

    @gql.field
    async def get_user(self, id: strawberry.ID) -> User:
        return await loader.load(id)


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
