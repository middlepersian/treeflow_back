import factory
from treeflow.corpus.models import SectionType


class SectionTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SectionType
        django_get_or_create = ('identifier',)

    identifier = factory.Faker("pystr", min_chars=3, max_chars=30)
