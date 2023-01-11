import factory
from mpcd.corpus.models import Codex


class CodexFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Codex

    sigle = factory.Faker("pystr",  max_chars=5)
