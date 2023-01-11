from factory import DjangoModelFactory, Faker
from mpcd.corpus.models import Dependency


class DependencyFactory(DjangoModelFactory):
    class Meta:
        model = Dependency

    head = SubFactory('mpcd.tests.factories.TokenFactory')
    rel = Faker("random_element", elements=["nsubj", "dobj", "ccomp", "pobj", "iobj"])
    producer = Faker("random_element", elements=[1, 2])
