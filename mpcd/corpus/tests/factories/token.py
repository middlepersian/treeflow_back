import factory
from mpcd.corpus.models import Token


class TokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Token

    number = factory.Faker("pyfloat", positive=True, left_digits=2, right_digits=2)

    #root = factory.Faker("pybool")
    #word_token = factory.Faker("pybool")
    #visible = factory.Faker("pybool")

    root = factory.LazyFunction(lambda: False)
    word_token = factory.LazyFunction(lambda: True)
    visible = factory.LazyFunction(lambda: True)

    text = factory.SubFactory("mpcd.corpus.tests.factories.TextFactory")
    language = factory.Faker("pystr", max_chars=3)
    transcription = factory.Faker("pystr", min_chars=5, max_chars=20)
    transliteration = factory.Faker("pystr", min_chars=5, max_chars=20)
    pos = factory.Faker("pystr", max_chars=5)

    avestan = factory.Faker("text")
    gloss = factory.Faker("text")

    lemmas = factory.RelatedFactory("mpcd.dict.tests.factories.LemmaFactory")
    meanings = factory.RelatedFactory("mpcd.dict.tests.factories.MeaningFactory")
    morphological_annotation = factory.RelatedFactory("mpcd.corpus.tests.factories.MorphologicalAnnotationFactory")
    #syntactic_annotation = factory.RelatedFactory("mpcd.corpus.tests.factories.DependencyFactory")
