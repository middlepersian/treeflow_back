from factory import DjangoModelFactory, Faker
from mpcd.corpus.models import MorphologicalAnnotation

class MorphologicalAnnotationFactory(DjangoModelFactory):
    class Meta:
        model = MorphologicalAnnotation

    feature = Faker("word", length=8)
    feature_value = Faker("word", length=8)
