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
        django_get_or_create = ("title", "corpus")
    corpus = factory.SubFactory(CorpusFactory)
    title = factory.Faker("pystr", min_chars=1, max_chars=30)
    text_sigle = factory.SubFactory(TextSigleFactory)
    stage = factory.Faker("pystr", max_chars=3  )

    editors = factory.RelatedFactory(UserFactory)
    authors = factory.RelatedFactory(UserFactory)
    collaborators = factory.RelatedFactory(UserFactory)
    sources = factory.RelatedFactory(SourceFactory)
    resources = factory.RelatedFactory(BibEntryFactory)

            
             