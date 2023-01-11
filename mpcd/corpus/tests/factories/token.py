import factory
from mpcd.corpus.models import Token


class TokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Token

    '''
    number = factory.Faker("pyfloat", positive=True, left_digits=2, right_digits=2)
    root = factory.Faker("pybool")
    word_token = factory.Faker("pybool")
    visible = factory.Faker("pybool")

    text = factory.SubFactory("mpcd.corpus.tests.factories.TextFactory")
    sentence = factory.SubFactory("mpcd.corpus.tests.factories.SentenceFactory")
    language = factory.Faker("language_code")
    transcription = factory.Faker("pystr", min_chars=5, max_chars=20)
    transliteration = factory.Faker("pystr", min_chars=5, max_chars=20)
    pos = factory.Faker("pystr", max_chars=5)

    avestan = factory.Faker("text")
    line = factory.SubFactory("mpcd.corpus.tests.factories.LineFactory")
    previous = factory.SubFactory("mpcd.corpus.tests.factories.TokenFactory", previous=None)
    gloss = factory.Faker("text")

    @factory.post_generation
    def set_previous(self, create, extracted, **kwargs):
        if kwargs.get('previous'):
            self.previous = kwargs.get('previous')

    @factory.post_generation
    def lemmas(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of lemmas were passed in, use them
            for lemma in extracted:
                self.lemmas.add(lemma)

    @factory.post_generation
    def meanings(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of meanings were passed in, use them
            for meaning in extracted:
                self.meanings.add(meaning)

    @factory.post_generation
    def morphological_annotation(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of morphological_annotations were passed in, use them
            for morphological_annotation in extracted:
                self.morphological_annotation.add(morphological_annotation)

    @factory.post_generation
    def syntactic_annotation(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of syntactic_annotations were passed in, use them
            for syntactic_annotation in extracted:
                self.syntactic_annotation.add(syntactic_annotation)
'''
