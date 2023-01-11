from factory import DjangoModelFactory, Faker, SubFactory
from mpcd.dict.models import Lemma
from .meaning import MeaningFactory

class LemmaFactory(DjangoModelFactory):
    class Meta:
        model = Lemma
    word = Faker("word")
    language = Faker("language_code")
    related_meanings = SubFactory(MeaningFactory)
    related_lemmas = SubFactory(LemmaFactory, related_lemmas=[], _quantity=3)
