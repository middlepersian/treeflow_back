import factory
from mpcd.corpus.models import Dependency


class DependencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dependency

    head = factory.SubFactory('mpcd.corpus.tests.factories.TokenFactory')
    rel = factory.Faker("random_element", elements=["nsubj", "dobj", "ccomp", "pobj", "iobj"])
    producer = factory.Faker("random_element", elements=[1, 2])
