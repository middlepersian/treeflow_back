import factory
from treeflow.corpus.models import Corpus


class CorpusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Corpus
        django_get_or_create = ('name', 'slug')

    name = factory.Faker("pystr", max_chars=20)
    slug = factory.Faker("pystr", max_chars=5)