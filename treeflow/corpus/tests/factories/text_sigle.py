import factory
from treeflow.corpus.models import TextSigle

class TextSigleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TextSigle

    sigle = factory.Faker("pystr", max_chars=10)
    genre = factory.Faker("pystr", max_chars=10)
