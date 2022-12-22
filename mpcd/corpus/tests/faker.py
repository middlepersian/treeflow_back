from typing import Generic, List, Type, TypeVar, cast

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, Group
import factory
from factory import fuzzy


import mpcd.corpus.models as models


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


# User

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


class CorpusFactory(_BaseFactory[models.Corpus]):
    class Meta:
        model = models.Corpus
    name = fuzzy.FuzzyText(length=100)
    slug = fuzzy.FuzzyText(length=10)



'''
# Comment
class CommentFactory(_BaseFactory[models.Comment]):
    class Meta:
        model = models.Comment

    text = factory.Faker("text")
    author = factory.SubFactory(UserFactory)


# Bibliography

class BibEntryFactory(_BaseFactory[models.BibEntry]):
    class Meta:
        model = models.BibEntry
    key = fuzzy.FuzzyText(length=3)


# Source
class SourceFactory(_BaseFactory[models.Source]):
    class Meta:
        model = models.Source

    identifier = factory.Faker("text")
    description = factory.Faker("text")
    #bib_entry = factory.SubFactory(BibEntryFactory)


# Codex
class CodexFactory(_BaseFactory[models.Codex]):
    class Meta:
        model = models.Codex
    identifier = fuzzy.FuzzyText(length=30)
    #bib_entry = factory.SubFactory(BibEntryFactory)
    history = fuzzy.FuzzyText(length=3)


# CodexPart
class CodexPartFactory(_BaseFactory[models.CodexPart]):
    class Meta:
        model = models.CodexPart
    #codex = fuzzy.SubFactory(CodexFactory)
    slug = fuzzy.FuzzyText(length=3)
    comments = fuzzy.FuzzyText(length=3)

# Corpus


class CorpusFactory(_BaseFactory[models.Corpus]):
    class Meta:
        model = models.Corpus
    name = fuzzy.FuzzyText(length=100)
    slug = fuzzy.FuzzyText(length=10)

# CustomSource


class CustomSourceFactory(_BaseFactory[models.CustomSource]):
    class Meta:
        model = models.CustomSource

# Dependency


class DependencyFactory(_BaseFactory[models.Dependency]):
    class Meta:
        model = models.Dependency
        # TODO solve circular dependency
    #head = fuzzy.SubFactory(TokenFactory)


class TextSigleFactory(_BaseFactory[models.TextSigle]):
    class Meta:
        model = models.TextSigle

    sigle = fuzzy.FuzzyText(length=10)
    genre = fuzzy.FuzzyText(length=3)


class TextFactory(_BaseFactory[models.Text]):
    class Meta:
        model = models.Text

    title = fuzzy.FuzzyText(length=100)
    text_sigle = factory.SubFactory(TextSigleFactory)
    stage = fuzzy.FuzzyText(length=3)
'''