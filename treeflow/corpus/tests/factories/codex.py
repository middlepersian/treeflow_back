import factory
from treeflow.corpus.models import Codex


class CodexFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Codex
        django_get_or_create = ('sigle',)

    sigle = factory.Faker("pystr",  max_chars=5)