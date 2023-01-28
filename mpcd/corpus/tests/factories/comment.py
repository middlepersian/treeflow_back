import factory
from mpcd.corpus.models import Comment


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory("mpcd.corpus.tests.factories.UserFactory")
    txt = factory.Faker("text")

    codex = factory.SubFactory("mpcd.corpus.tests.factories.CodexFactory")
    dependency = factory.SubFactory("mpcd.corpus.tests.factories.DependencyFactory")
    edition = factory.SubFactory("mpcd.corpus.tests.factories.EditionFactory")
    facsimile = factory.SubFactory("mpcd.corpus.tests.factories.FacsimileFactory")
    folio = factory.SubFactory("mpcd.corpus.tests.factories.FolioFactory")
    line = factory.SubFactory("mpcd.corpus.tests.factories.LineFactory")
    resource = factory.SubFactory("mpcd.corpus.tests.factories.ResourceFactory")
    section_type = factory.SubFactory("mpcd.corpus.tests.factories.SectionTypeFactory")
    section = factory.SubFactory("mpcd.corpus.tests.factories.SectionFactory")
    sentence = factory.SubFactory("mpcd.corpus.tests.factories.SentenceFactory")
    text_sigle = factory.SubFactory("mpcd.corpus.tests.factories.TextSigleFactory")
    text = factory.SubFactory("mpcd.corpus.tests.factories.TextFactory")

    token = factory.SubFactory("mpcd.corpus.tests.factories.TokenFactory")
    uncertain = factory.List(["a", "b", "c"])
    to_discuss = factory.List(["d", "e", "f"])
    new_suggestion = factory.List(["g", "h", "i"])
