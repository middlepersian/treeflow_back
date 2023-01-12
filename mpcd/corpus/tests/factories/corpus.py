import factory
from mpcd.corpus.models import Corpus


class CorpusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Corpus

    name = factory.Faker("pystr", max_chars=3)
    slug = factory.Faker("pystr", max_chars=3)