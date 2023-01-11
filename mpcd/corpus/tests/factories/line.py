import factory
from mpcd.corpus.models import Line

class LineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Line

    identifier = factory.Faker("pystr", min_chars=5, max_chars=10)
    folio = factory.SubFactory("mpcd.corpus.tests.factories.FolioFactory")
    number = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    number_in_text = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    previous = factory.SubFactory("mpcd.corpus.tests.factories.LineFactory", previous=None)

    @factory.post_generation
    def set_previous(self, create, extracted, **kwargs):
        if kwargs.get('previous'):
            self.previous = kwargs.get('previous')
