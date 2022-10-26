from typing import Generic, List, Type, TypeVar, cast

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, Group
import factory


from mpcd.corpus.models import Comment

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


class UserFactory(_BaseFactory["User"]):
    class Meta:
        model = User

    is_active = True
    username = factory.Faker("username")
    username = factory.Sequence(lambda n: f"username-{n}")
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: make_password("foobar"))


class StaffUserFactory(UserFactory):
    is_staff = True


class SuperuserUserFactory(UserFactory):
    is_superuser = True


class CommentFactory(_BaseFactory[Comment]):
    class Meta:
        model = Comment

    text = factory.Faker("text")
    author = factory.SubFactory(UserFactory)