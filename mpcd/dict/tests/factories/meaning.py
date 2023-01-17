import factory
from mpcd.dict.models import Meaning


class MeaningFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Meaning
        django_get_or_create = ("meaning", "language")

    meaning = factory.Faker("word")
    language = factory.Faker("pystr", max_chars=3)

    @factory.post_generation
    def related_meanings(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of meanings were passed in, use them
            for meaning in extracted:
                self.related_meanings.add(meaning)
