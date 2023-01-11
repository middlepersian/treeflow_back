import factory
from mpcd.corpus.models import Sentence

class SentenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sentence

    number = factory.Faker("pyfloat", left_digits=1, right_digits=2, positive=True)
    text = factory.SubFactory("mpcd.corpus.tests.factories.TextFactory")
    meanings = factory.SubFactory("mpcd.corpus.tests.factories.MeaningFactory")
    previous = factory.SubFactory("self")

    comment_sentence = factory.RelatedFactory(CommentFactory, "sentence", size=2)
    token_sentence = factory.RelatedFactory(TokenFactory, "sentence", size=2)
