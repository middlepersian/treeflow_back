import factory
from treeflow.corpus.models import Text
from treeflow.corpus.tests.factories import CorpusFactory
from treeflow.corpus.tests.factories import SourceFactory
from treeflow.corpus.tests.factories import BibEntryFactory
from treeflow.users.tests.factories import UserFactory

class TextFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Text
        django_get_or_create = ("title", "corpus")
    corpus = factory.SubFactory(CorpusFactory)
    title = factory.Faker("pystr", min_chars=1, max_chars=30)
    language = factory.List([factory.Faker("pystr", min_chars=1, max_chars=3)])
    series = factory.Faker("pystr", min_chars=1, max_chars=20)
    label = factory.Faker("pystr", min_chars=1, max_chars=20)
    stage = factory.Faker("pystr", max_chars=3)

    editors = factory.RelatedFactory(UserFactory)
    collaborators = factory.RelatedFactory(UserFactory)

    sources = factory.RelatedFactory(SourceFactory)
