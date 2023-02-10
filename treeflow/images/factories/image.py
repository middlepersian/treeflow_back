import factory
from treeflow.images.models import Image


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image
    identifier = factory.Faker("word")
    number = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    source = factory.SubFactory("treeflow.corpus.tests.factories.source.SourceFactory")

    @factory.post_generation
    def sections(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for section in extracted:
                self.sections.add(section)


    @factory.post_generation
    def set_previous(self, create, extracted, **kwargs):
        if kwargs.get('previous'):
            self.previous = kwargs.get('previous')