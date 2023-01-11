from factory import DjangoModelFactory, SubFactory, Faker
from mpcd.corpus.models import Section

class SectionFactory(DjangoModelFactory):
    class Meta:
        model = Section

    number = factory.Faker("pyfloat", positive=True, left_digits=2, right_digits=2)
    identifier = factory.Faker("word", length=10)
    text = SubFactory("mpcd.corpus.tests.factories.TextFactory")
    section_type = SubFactory("mpcd.corpus.tests.factories.SectionTypeFactory")
    source = SubFactory("mpcd.corpus.tests.factories.SourceFactory")
    tokens = SubFactory("mpcd.corpus.tests.factories.TokenFactory", _quantity=5)
    previous = SubFactory("self")
    container = SubFactory("self")
