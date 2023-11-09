
from typing import Type, cast
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
import factory


User = cast(Type[AbstractUser], get_user_model())


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    is_active = True
    username = factory.Sequence(lambda n: f"username-{n}")
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: make_password("foobar"))
