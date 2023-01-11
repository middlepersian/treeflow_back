

import factory
from mpcd.corpus.models import Corpus


class CorpusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Corpus

    name = factory.Faker("word")
    slug = factory.Faker("word")