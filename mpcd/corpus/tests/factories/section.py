import factory
from mpcd.corpus.models import Section


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Section

    number = factory.Faker("pyfloat", positive=True, left_digits=2, right_digits=2)
    identifier = factory.Faker("pystr", min_chars=1, max_chars=10)
    text = factory.SubFactory("mpcd.corpus.tests.factories.TextFactory")
    section_type = factory.SubFactory("mpcd.corpus.tests.factories.SectionTypeFactory")
    source = factory.SubFactory("mpcd.corpus.tests.factories.SourceFactory")

    @factory.post_generation
    def set_previous(self, create, extracted, **kwargs):
        if kwargs.get('previous'):
            self.previous = kwargs.get('previous')

    @factory.post_generation
    def set_container(self, create, extracted, **kwargs):
        if kwargs.get('container'):
            self.container = kwargs.get('container')

    @factory.post_generation
    def set_tokens(self, create, extracted, **kwargs):
        if kwargs.get('tokens'):
            self.tokens.set(kwargs.get('tokens'))
