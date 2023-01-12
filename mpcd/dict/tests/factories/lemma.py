from factory import Faker, SubFactory
import factory
from factory.django import DjangoModelFactory
from mpcd.dict.models import Lemma


class LemmaFactory(DjangoModelFactory):
    class Meta:
        model = Lemma

    word = Faker("word")
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
    @factory.post_generation
    def related_lemmas(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of lemmas were passed in, use them
            for lemma in extracted:
                self.related_lemmas.add(lemma)