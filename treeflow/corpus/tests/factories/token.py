import factory
from treeflow.corpus.models import Token


class TokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Token
        django_get_or_create = ("number", "text")

    number = factory.Faker("pyfloat", positive=True)
    number_in_sentence = factory.Faker("pylist", nb_elements=10, variable_nb_elements=True, value_types="int")

    root = factory.LazyFunction(lambda: False)
    word_token = factory.LazyFunction(lambda: True)
    visible = factory.LazyFunction(lambda: True)

    text = factory.SubFactory("treeflow.corpus.tests.factories.TextFactory")
    language = factory.Faker("pystr", max_chars=3)
    transcription = factory.Faker("pystr", min_chars=5, max_chars=20)
    transliteration = factory.Faker("pystr", min_chars=5, max_chars=20)
    upos = factory.Faker("pystr", max_chars=5)
    xpos = factory.Faker('pylist', nb_elements=10, variable_nb_elements=True, value_types='str')
    avestan = factory.Faker("text")
    gloss = factory.Faker("text")

    lemmas = factory.RelatedFactory("treeflow.dict.tests.factories.LemmaFactory")
    meanings = factory.RelatedFactory("treeflow.dict.tests.factories.MeaningFactory")
    postfeatures = factory.RelatedFactory("treeflow.corpus.tests.factories.PostFeatureFactory")
    dependencies = factory.RelatedFactory("treeflow.corpus.tests.factories.DependencyFactory")


    multiword_token = factory.LazyFunction(lambda: False)
    created_at = factory.Faker("date_time")
    updated_at = factory.Faker("date_time")

    @factory.post_generation
    def related_tokens(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for token in extracted:
                self.related_tokens.add(token)
    @factory.post_generation
    def previous(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.previous = extracted             