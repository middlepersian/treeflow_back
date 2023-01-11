import factory
from mpcd.corpus.models import Sentence


class SentenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sentence

    number = factory.Faker("pyfloat", left_digits=1, right_digits=2, positive=True)
    text = factory.SubFactory("mpcd.corpus.tests.factories.TextFactory")
    meanings = factory.RelatedFactory("mpcd.corpus.tests.factories.MeaningFactory", "sentence", size=2)
    previous = factory.LazyAttribute("mpcd.corpus.tests.factories.SentenceFactory")
    comment_sentence = factory.RelatedFactory("mpcd.corpus.tests.factories.CommentFactory", "sentence", size=2)
    token_sentence = factory.RelatedFactory("mpcd.corpus.tests.factories.TokenFactory", "sentence", size=2)
