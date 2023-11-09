import factory
from treeflow.corpus.models import Dependency


class DependencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dependency

    rel = factory.Faker("pystr", min_chars=1, max_chars=25)
    producer = factory.Faker("random_element", elements=[1, 2])
    head_number = factory.Faker("pyfloat", left_digits=2, right_digits=3, positive=True)

    created_at = factory.Faker("date_time")
    updated_at = factory.Faker("date_time")

    @factory.post_generation
    def head(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            # A list of tokens were passed in, use them
            for token in extracted:
                self.head.add(token)