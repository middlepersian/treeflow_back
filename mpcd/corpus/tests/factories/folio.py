from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

class FolioFactory(DjangoModelFactory):
    class Meta:
        model = Folio
    identifier = factory.Faker("word")
    number = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    facsimile = SubFactory("mpcd.corpus.tests.factories.FacsimileFactory")
    comments = SubFactory("mpcd.corpus.tests.factories.CommentFactory", comments=None)
    previous = SubFactory("self", next=None)