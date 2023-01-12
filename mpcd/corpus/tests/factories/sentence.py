import factory
from mpcd.corpus.models import Sentence


class SentenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sentence

    number = factory.Faker("pyfloat", left_digits=1, right_digits=2, positive=True)
    text = factory.SubFactory("mpcd.corpus.tests.factories.TextFactory")
    meanings = factory.RelatedFactory("mpcd.dict.tests.factories.MeaningFactory")