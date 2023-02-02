from typing import Generic, List, Type, TypeVar, cast

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, Group
import factory
from factory import fuzzy


import treeflow.dict.models as models


_T = TypeVar("_T")
User = cast(Type[AbstractUser], get_user_model())


class _BaseFactory(Generic[_T], factory.django.DjangoModelFactory):
    @classmethod
    def create(cls, **kwargs) -> _T:
        return super().create(**kwargs)

    @classmethod
    def create_batch(cls, size: int, **kwargs) -> List[_T]:
        return super().create_batch(size, **kwargs)


class GroupFactory(_BaseFactory[Group]):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: f"Group {n}")


# Lemma

class LemmaFactory(_BaseFactory[models.Lemma]):
    class Meta:
        model = Lemma

    word = factory.Sequence(lambda n: f"Word {n}")
    #language = factory.Sequence(lambda n: f"Language {n}")
