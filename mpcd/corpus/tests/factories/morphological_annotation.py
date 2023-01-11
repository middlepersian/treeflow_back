import factory
from mpcd.corpus.models import MorphologicalAnnotation


class MorphologicalAnnotationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MorphologicalAnnotation

    feature = factory.Faker("pystr", min_chars=1, max_chars=3)
    feature_value = factory.Faker("pystr", min_chars=1, max_chars=3)
