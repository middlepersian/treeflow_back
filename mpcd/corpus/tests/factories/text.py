import factory
from mpcd.corpus.models import Text
from mpcd.corpus.tests.factories.corpus import CorpusFactory
from mpcd.corpus.tests.factories.text_sigle import TextSigleFactory
from mpcd.corpus.tests.factories.source import SourceFactory
from mpcd.corpus.tests.factories.bibliography import BibEntryFactory
from mpcd.users.tests.factories import UserFactory

class TextFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Text
    corpus = factory.SubFactory(CorpusFactory)
    title = factory.Faker("pystr", min_chars=1, max_chars=10)
    text_sigle = factory.SubFactory(TextSigleFactory)
    stage = factory.Faker("pystr", max_chars=3)
    sources = factory.SubFactory(SourceFactory)
    resources = factory.SubFactory(BibEntryFactory)
    editors = factory.SubFactory(UserFactory)
    collaborators = factory.SubFactory(UserFactory)
