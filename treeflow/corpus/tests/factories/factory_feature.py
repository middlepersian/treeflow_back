import factory
from treeflow.corpus.models import Feature


class FeatureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feature

        django_get_or_create = ('feature', 'feature_value')

    feature = factory.Faker("pystr", min_chars=1, max_chars=3)
    feature_value = factory.Faker("pystr", min_chars=1, max_chars=3)
