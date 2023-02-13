import factory
from treeflow.corpus.models import Section


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Section
        django_get_or_create = ('text', 'identifier')

    number = factory.Faker("pyfloat", positive=True, left_digits=2, right_digits=2)
    identifier = factory.Faker("pystr", min_chars=1, max_chars=10)
    title = factory.Faker("pystr", min_chars=3, max_chars=20)
    language = factory.Faker("pystr", max_chars=3)
    text = factory.SubFactory("treeflow.corpus.tests.factories.TextFactory")
    section_type = factory.SubFactory("treeflow.corpus.tests.factories.SectionTypeFactory")
    source = factory.SubFactory("treeflow.corpus.tests.factories.SourceFactory")

    tokens = factory.RelatedFactory("treeflow.corpus.tests.factories.TokenFactory")

    @factory.post_generation
    def set_previous(self, create, extracted, **kwargs):
        if kwargs.get('previous'):
            self.previous = kwargs.get('previous')

    @factory.post_generation
    def set_container(self, create, extracted, **kwargs):
        if kwargs.get('container'):
            self.container = kwargs.get('container')

    @factory.post_generation
    def meanings(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for meaning in extracted:
                self.meanings.add(meaning)        
