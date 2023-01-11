from factory import DjangoModelFactory, Faker
from mpcd.dict.models import Meaning


class MeaningFactory(DjangoModelFactory):
    class Meta:
        model = Meaning
    meaning = Faker("sentence", nb_words=3)
    language = Faker("language_code")
    related_meanings = SubFactory("self", _quantity=3)
