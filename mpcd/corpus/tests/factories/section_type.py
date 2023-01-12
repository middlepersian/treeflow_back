import factory
from mpcd.corpus.models import SectionType

class SectionTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SectionType
    
    identifier = factory.Faker("pystr", min_chars=5, max_chars=30)