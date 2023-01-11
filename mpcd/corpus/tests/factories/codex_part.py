import factory
from faker import Faker


class CodexPartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CodexPart

    slug = factory.Faker("slug")
    codex = factory.SubFactory(CodexFactory)


