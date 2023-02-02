import factory
from treeflow.images.models import Image


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image
    identifier = factory.Faker("word")
    number = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    facsimile = factory.SubFactory("treeflow.images.factories.FacsimileFactory")
    sections = factory.RelatedFactory("treeflow.corpus.tests.factories.SectionFactory")
    @factory.post_generation
    def set_previous(self, create, extracted, **kwargs):
        if kwargs.get('previous'):
            self.previous = kwargs.get('previous')