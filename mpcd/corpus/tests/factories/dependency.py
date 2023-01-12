import factory
from mpcd.corpus.models import Dependency


class DependencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dependency

    rel = factory.Faker("random_element", elements=["nsubj", "dobj", "ccomp", "pobj", "iobj"])
    producer = factory.Faker("random_element", elements=[1, 2])

    @factory.post_generation
    def head(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            # A list of tokens were passed in, use them
            for token in extracted:
                self.head.add(token)