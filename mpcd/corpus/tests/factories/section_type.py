import factory
from mpcd.corpus.models import SectionType

class SectionTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SectionType
    
    identifier = factory.Faker('word')
