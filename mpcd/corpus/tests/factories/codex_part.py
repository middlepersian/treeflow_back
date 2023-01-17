import factory
from mpcd.corpus.models import CodexPart


class CodexPartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CodexPart
        django_get_or_create = ('slug',)

    slug = factory.Faker("pystr", max_chars=5)
    codex = factory.SubFactory("mpcd.corpus.tests.factories.CodexFactory")
