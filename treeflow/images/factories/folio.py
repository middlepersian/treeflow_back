import factory
from treeflow.corpus.models import Folio


class FolioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Folio
    identifier = factory.Faker("word")
    number = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    facsimile = factory.SubFactory("treeflow.corpus.tests.factories.FacsimileFactory")
    sections = factory.RelatedFactory("treeflow.corpus.tests.factories.SectionFactory")
    @factory.post_generation
    def set_previous(self, create, extracted, **kwargs):
        if kwargs.get('previous'):
            self.previous = kwargs.get('previous')