import factory
from mpcd.corpus.models import CodexPart
from mpcd.corpus.tests.factories.codex import CodexFactory

class CodexPartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CodexPart

    slug = factory.Faker("slug")
    codex = factory.SubFactory(CodexFactory)

