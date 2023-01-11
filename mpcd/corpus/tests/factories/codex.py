import factory
from faker import Faker


class CodexFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Codex

    sigle = factory.Faker("pystr",  max_chars=5)
