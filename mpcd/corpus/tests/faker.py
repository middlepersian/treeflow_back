from typing import Generic, List, Type, TypeVar, cast

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, Group
import factory
from factory import fuzzy


from mpcd.corpus.models import Comment, Text, TextSigle, Corpus

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


class CommentFactory(_BaseFactory["Comment"]):
    class Meta:
        model = Comment

    text = factory.Faker("text")
    author = factory.SubFactory(UserFactory)



class TextSigleFactory(_BaseFactory["TextSigle"]):
    class Meta:
        model = TextSigle

    sigle = fuzzy.FuzzyText(length=10)
    genre = fuzzy.FuzzyText(length=3)


class TextFactory(_BaseFactory["Text"]):
    class Meta:
        model = Text

    title = fuzzy.FuzzyText(length=100)
    text_sigle = factory.SubFactory(TextSigleFactory)
    stage = fuzzy.FuzzyText(length=3)
